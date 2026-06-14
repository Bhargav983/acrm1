import json
import urllib.error
import urllib.request
from datetime import date, datetime
from decimal import Decimal, InvalidOperation

from django.db.models import Q
from django.utils import timezone

from core.models import AppConfig

from .forms import (
    ASTROLOGY_PLANETS,
    NAKSHATRA_LORDS,
    SIGN_LORDS,
    destination_sign_from_house,
    planet_relationship,
)
from .models import APIData


FREE_ASTROLOGY_BASE_URL = 'https://json.freeastrologyapi.com'

CHART_PLANET_NAMES = {
    'Ascendant',
    'Sun',
    'Moon',
    'Mars',
    'Mercury',
    'Jupiter',
    'Venus',
    'Saturn',
    'Rahu',
    'Ketu',
}
DASHA_PLANET_ORDER = (
    'Ketu',
    'Venus',
    'Sun',
    'Moon',
    'Mars',
    'Rahu',
    'Jupiter',
    'Saturn',
    'Mercury',
)

NAKSHATRA_NORMALIZATION = {
    'Aaslesha': 'Ashlesha',
    'Aslesha': 'Ashlesha',
    'Jyeshta': 'Jyeshtha',
    'Makha': 'Magha',
    'Mrigasira': 'Mrigashira',
    'Pushyami': 'Pushya',
    'Visakha': 'Vishakha',
}


class FreeAstrologyAPIError(Exception):
    pass


def get_free_astrology_config():
    config = (
        AppConfig.objects.filter(config_type='Astrology API', is_active=True)
        .filter(Q(provider_name__icontains='free') | Q(config_name__icontains='free'))
        .first()
    )
    if not config:
        config = AppConfig.objects.filter(config_type='Astrology API', is_active=True).first()
    if not config or not config.api_key:
        raise FreeAstrologyAPIError(
            'Active Astrology API configuration with API key is required.'
        )
    return config


def endpoint_url(config, endpoint):
    base_url = (config.api_url or FREE_ASTROLOGY_BASE_URL).rstrip('/')
    if base_url.endswith(endpoint):
        return base_url
    return f'{base_url}/{endpoint}'


def post_json(config, endpoint, payload):
    request = urllib.request.Request(
        endpoint_url(config, endpoint),
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'Content-Type': 'application/json',
            'x-api-key': config.api_key,
        },
        method='POST',
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as error:
        detail = error.read().decode('utf-8', errors='replace')
        raise FreeAstrologyAPIError(f'API returned {error.code}: {detail}') from error
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
        raise FreeAstrologyAPIError(f'API request failed: {error}') from error


def normalize_nakshatra(value):
    return NAKSHATRA_NORMALIZATION.get(value, value or '')


def house_label(number):
    suffix = 'th'
    if number % 100 not in [11, 12, 13]:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(number % 10, 'th')
    return f'{number}{suffix} House'


def decimal_value(value):
    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError):
        return None


def fetch_geo_details(customer):
    if not customer.place_of_birth:
        raise FreeAstrologyAPIError('Place of birth is required before fetching location.')

    config = get_free_astrology_config()
    location_queries = [customer.place_of_birth]
    city_name = customer.place_of_birth.split(',')[0].strip()
    if city_name and city_name not in location_queries:
        location_queries.append(city_name)

    response = None
    locations = []
    matched_query = ''
    for location_query in location_queries:
        payload = {'location': location_query}
        response = post_json(config, 'geo-details', payload)
        locations = geo_locations_from_response(response)
        if locations:
            matched_query = location_query
            break
    if not locations:
        raise FreeAstrologyAPIError('No location details returned for this place.')

    location = locations[0]
    latitude = decimal_value(location.get('latitude'))
    longitude = decimal_value(location.get('longitude'))
    if latitude is None or longitude is None:
        raise FreeAstrologyAPIError('Location response did not include valid coordinates.')

    customer.latitude = latitude
    customer.longitude = longitude
    customer.timezone = str(location.get('timezone') or location.get('timezone_offset') or '')
    customer.save(update_fields=['latitude', 'longitude', 'timezone', 'updated_at'])
    location['matched_query'] = matched_query
    return location


def search_geo_locations(query):
    query = (query or '').strip()
    if len(query) < 3:
        return []

    config = get_free_astrology_config()
    location_queries = [query]
    city_name = query.split(',')[0].strip()
    if city_name and city_name not in location_queries:
        location_queries.append(city_name)

    for location_query in location_queries:
        response = post_json(config, 'geo-details', {'location': location_query})
        locations = geo_locations_from_response(response)
        if locations:
            return [
                {
                    'label': location.get('complete_name')
                    or location.get('location_name')
                    or location_query,
                    'location_name': location.get('location_name', ''),
                    'complete_name': location.get('complete_name', ''),
                    'latitude': location.get('latitude'),
                    'longitude': location.get('longitude'),
                    'timezone': location.get('timezone') or location.get('timezone_offset') or '',
                    'timezone_offset': location.get('timezone_offset'),
                    'country': location.get('country', ''),
                    'administrative_zone_1': location.get('administrative_zone_1', ''),
                    'administrative_zone_2': location.get('administrative_zone_2', ''),
                }
                for location in locations[:8]
            ]
    return []


def geo_locations_from_response(response):
    if isinstance(response, list):
        return response
    if not isinstance(response, dict):
        return []
    for key in ['output', 'data', 'results', 'locations']:
        value = response.get(key)
        if isinstance(value, list):
            return value
    if {'latitude', 'longitude'}.issubset(response.keys()):
        return [response]
    return []


def timezone_offset_from_customer(customer, geo_details=None):
    if geo_details and geo_details.get('timezone_offset') is not None:
        return float(geo_details['timezone_offset'])
    try:
        return float(customer.timezone)
    except (TypeError, ValueError):
        return None


def ensure_geo_for_astrology(customer):
    geo_details = None
    if not customer.latitude or not customer.longitude:
        geo_details = fetch_geo_details(customer)
    timezone_offset = timezone_offset_from_customer(customer, geo_details)
    if timezone_offset is None and customer.place_of_birth:
        geo_details = fetch_geo_details(customer)
        timezone_offset = timezone_offset_from_customer(customer, geo_details)
    if timezone_offset is None:
        raise FreeAstrologyAPIError('Numeric timezone offset is required for astrology API.')
    return geo_details, timezone_offset


def build_planets_payload(customer, timezone_offset):
    if not customer.date_of_birth or not customer.time_of_birth:
        raise FreeAstrologyAPIError('Date of birth and time of birth are required.')
    if customer.latitude is None or customer.longitude is None:
        raise FreeAstrologyAPIError('Latitude and longitude are required.')

    return {
        'year': customer.date_of_birth.year,
        'month': customer.date_of_birth.month,
        'date': customer.date_of_birth.day,
        'hours': customer.time_of_birth.hour,
        'minutes': customer.time_of_birth.minute,
        'seconds': customer.time_of_birth.second,
        'latitude': float(customer.latitude),
        'longitude': float(customer.longitude),
        'timezone': timezone_offset,
        'settings': {
            'observation_point': 'topocentric',
            'ayanamsha': 'lahiri',
            'language': 'en',
        },
    }


def build_vimsottari_payload(planets_payload):
    payload = dict(planets_payload)
    settings = payload.pop('settings', {})
    payload['config'] = {
        'observation_point': settings.get('observation_point', 'topocentric'),
        'ayanamsha': settings.get('ayanamsha', 'lahiri'),
    }
    return payload


def planet_output(response):
    output = response.get('output', response)
    if not isinstance(output, dict):
        raise FreeAstrologyAPIError('Planets response did not contain expected output.')
    return output


def chart_positions_from_output(output):
    positions = []
    for key, planet in output.items():
        if not isinstance(planet, dict):
            continue
        name = planet.get('name') or planet.get('localized_name') or key
        if name not in CHART_PLANET_NAMES:
            continue
        current_sign = planet.get('current_sign')
        if current_sign in (None, ''):
            continue
        try:
            current_sign = int(current_sign)
        except (TypeError, ValueError):
            continue
        if current_sign < 1 or current_sign > 12:
            continue
        positions.append(
            {
                'name': name,
                'current_sign': current_sign,
                'house_number': planet.get('house_number') or '',
                'is_retrograde': str(planet.get('isRetro', '')).lower() == 'true',
            }
        )
    return positions


def parse_api_date(value):
    if not value:
        return None
    if isinstance(value, date):
        return value
    try:
        return datetime.strptime(str(value)[:10], '%Y-%m-%d').date()
    except ValueError:
        return None


def dasha_rows_from_output(output):
    rows = []
    maha_names = [name for name in DASHA_PLANET_ORDER if name in output]
    maha_names.extend(name for name in output if name not in maha_names)
    for maha_name in maha_names:
        antar_periods = output.get(maha_name, {})
        if not isinstance(antar_periods, dict):
            continue
        antar_names = [name for name in DASHA_PLANET_ORDER if name in antar_periods]
        antar_names.extend(name for name in antar_periods if name not in antar_names)
        for antar_name in antar_names:
            period = antar_periods.get(antar_name, {})
            if not isinstance(period, dict):
                continue
            rows.append(
                {
                    'maha_dasha': maha_name,
                    'antar_dasha': antar_name,
                    'start_time': period.get('start_time', ''),
                    'end_time': period.get('end_time', ''),
                }
            )
    return rows


def current_dasha_from_rows(rows, on_date=None):
    on_date = on_date or timezone.localdate()
    for row in rows:
        start_date = parse_api_date(row.get('start_time'))
        end_date = parse_api_date(row.get('end_time'))
        if start_date and end_date and start_date <= on_date < end_date:
            return row
    return {}


def map_planets_to_manual_entries(output):
    manual_entries = {}
    for slug, planet_name in ASTROLOGY_PLANETS:
        planet = output.get(planet_name, {})
        sign = planet.get('zodiac_sign_name', '')
        sign_lord = planet.get('zodiac_sign_lord') or SIGN_LORDS.get(sign, '')
        house_number = planet.get('house_number')
        nakshatra = normalize_nakshatra(planet.get('nakshatra_name'))
        nakshatra_owner = planet.get('nakshatra_vimsottari_lord') or NAKSHATRA_LORDS.get(
            nakshatra,
            '',
        )

        if sign:
            manual_entries[f'planet_sign_{slug}'] = sign
            manual_entries[f'planet_sign_{slug}_lord'] = sign_lord
            manual_entries[f'planet_sign_{slug}_relationship'] = planet_relationship(
                planet_name,
                sign_lord,
            )
        if house_number:
            manual_entries[f'planet_house_{slug}'] = house_label(int(house_number))
        if nakshatra:
            manual_entries[f'planet_nakshatra_{slug}'] = nakshatra
            manual_entries[f'planet_nakshatra_{slug}_pada'] = str(
                planet.get('nakshatra_pada') or ''
            )
            manual_entries[f'planet_nakshatra_{slug}_owner'] = nakshatra_owner
            manual_entries[f'planet_nakshatra_{slug}_relationship'] = planet_relationship(
                planet_name,
                nakshatra_owner,
            )

    ascendant = output.get('Ascendant', {})
    lagna = ascendant.get('zodiac_sign_name', '')
    if lagna:
        for house_number in range(1, 13):
            source_sign = destination_sign_from_house(lagna, house_label(house_number))
            lord_planet = SIGN_LORDS.get(source_sign, '')
            lord_output = output.get(lord_planet, {})
            destination_house = (
                house_label(int(lord_output['house_number']))
                if lord_output.get('house_number')
                else ''
            )
            destination_sign = lord_output.get('zodiac_sign_name') or (
                destination_sign_from_house(lagna, destination_house)
                if destination_house
                else ''
            )
            manual_entries[f'house_lord_{house_number}_source_sign'] = source_sign
            manual_entries[f'house_lord_{house_number}_lord_planet'] = lord_planet
            if destination_house:
                manual_entries[f'house_lord_{house_number}_destination_house'] = destination_house
            if destination_sign:
                manual_entries[f'house_lord_{house_number}_destination_sign'] = destination_sign
                manual_entries[f'house_lord_{house_number}_relationship'] = planet_relationship(
                    lord_planet,
                    SIGN_LORDS.get(destination_sign, ''),
                )
    return manual_entries


def create_astrology_data_from_api(customer):
    config = get_free_astrology_config()
    geo_details, timezone_offset = ensure_geo_for_astrology(customer)
    payload = build_planets_payload(customer, timezone_offset)
    response = post_json(config, 'planets/extended', payload)
    output = planet_output(response)
    api_warnings = []
    navamsa_response = None
    navamsa_output = {}
    vimsottari_response = None
    vimsottari_output = {}
    try:
        navamsa_response = post_json(config, 'navamsa-chart-info', payload)
        navamsa_output = planet_output(navamsa_response)
    except FreeAstrologyAPIError as error:
        api_warnings.append(f'D9 Navamsa data was not fetched: {error}')
    try:
        vimsottari_payload = build_vimsottari_payload(payload)
        vimsottari_response = post_json(
            config,
            'vimsottari/maha-dasas-and-antar-dasas',
            vimsottari_payload,
        )
        vimsottari_output = planet_output(vimsottari_response)
    except FreeAstrologyAPIError as error:
        api_warnings.append(f'Vimsottari Dasha data was not fetched: {error}')

    ascendant = output.get('Ascendant', {})
    moon = output.get('Moon', {})
    sun = output.get('Sun', {})
    manual_entries = map_planets_to_manual_entries(output)
    dasha_rows = dasha_rows_from_output(vimsottari_output)
    current_dasha = current_dasha_from_rows(dasha_rows)
    parsed_response = {
        'manual_entries': manual_entries,
        'geo_details': geo_details,
        'planets_extended': output,
        'navamsa_chart_info': navamsa_output,
        'vimsottari_maha_dasas_and_antar_dasas': vimsottari_output,
        'vimsottari_dasha_rows': dasha_rows,
        'charts': {
            'd1': chart_positions_from_output(output),
            'd9': chart_positions_from_output(navamsa_output),
        },
    }
    if api_warnings:
        parsed_response['api_warnings'] = api_warnings

    return APIData.objects.create(
        customer=customer,
        data_source='api',
        api_provider=config.provider_name or 'Free Astrology API',
        api_name='planets/extended + navamsa-chart-info + vimsottari',
        api_type='birth_chart',
        request_parameters={
            'geo_lookup_used': bool(geo_details),
            'planets_payload': payload,
            'vimsottari_payload': build_vimsottari_payload(payload),
        },
        lagna=ascendant.get('zodiac_sign_name', ''),
        moon_sign=moon.get('zodiac_sign_name', ''),
        sun_sign=sun.get('zodiac_sign_name', ''),
        nakshatra=normalize_nakshatra(moon.get('nakshatra_name')),
        pada=moon.get('nakshatra_pada') or None,
        current_mahadasha=current_dasha.get('maha_dasha', ''),
        current_antardasha=current_dasha.get('antar_dasha', ''),
        raw_api_response={
            'geo_details': geo_details,
            'planets_extended': response,
            'navamsa_chart_info': navamsa_response,
            'vimsottari_maha_dasas_and_antar_dasas': vimsottari_response,
        },
        parsed_response=parsed_response,
        notes=(
            'Created from Free Astrology API planets/extended, navamsa-chart-info, and vimsottari.'
            if not api_warnings
            else 'Created from Free Astrology API planets/extended. ' + ' '.join(api_warnings)
        ),
    )
