from flask import Flask, render_template, request, jsonify
import math
from datetime import datetime

app = Flask(__name__)

def convert_age(birth_date):
    today = datetime.now().date()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

def convert_currency(amount, from_currency, to_currency):
    conversion_rates = {
    'USD': {'EUR': 0.93, 'GBP': 0.79, 'JPY': 153.24, 'INR': 83.39, 'AUD': 1.52, 'CAD': 1.37, 'CHF': 0.91, 'CNY': 7.24, 'HKD': 7.83, 'NZD': 1.67, 'KRW': 1358.23, 'SGD': 1.35, 'MXN': 16.97, 'BRL': 5.12, 'ZAR': 18.72, 'RUB': 92.45, 'TRY': 32.25, 'AED': 3.67, 'SAR': 3.75, 'BDT': 109.50},
    'EUR': {'USD': 1.08, 'GBP': 0.85, 'JPY': 165.12, 'INR': 89.78, 'AUD': 1.64, 'CAD': 1.48, 'CHF': 0.98, 'CNY': 7.81, 'HKD': 8.45, 'NZD': 1.80, 'KRW': 1463.45, 'SGD': 1.46, 'MXN': 18.30, 'BRL': 5.52, 'ZAR': 20.18, 'RUB': 99.75, 'TRY': 34.80, 'AED': 3.96, 'SAR': 4.04, 'BDT': 118.20},
    'GBP': {'USD': 1.27, 'EUR': 1.18, 'JPY': 194.56, 'INR': 105.67, 'AUD': 1.93, 'CAD': 1.74, 'CHF': 1.15, 'CNY': 9.20, 'HKD': 9.95, 'NZD': 2.12, 'KRW': 1725.89, 'SGD': 1.72, 'MXN': 21.60, 'BRL': 6.52, 'ZAR': 23.83, 'RUB': 117.82, 'TRY': 41.12, 'AED': 4.67, 'SAR': 4.76, 'BDT': 139.45},
    'JPY': {'USD': 0.0065, 'EUR': 0.0061, 'GBP': 0.0051, 'INR': 0.54, 'AUD': 0.0099, 'CAD': 0.0089, 'CHF': 0.0059, 'CNY': 0.047, 'HKD': 0.051, 'NZD': 0.011, 'KRW': 8.86, 'SGD': 0.0088, 'MXN': 0.11, 'BRL': 0.033, 'ZAR': 0.12, 'RUB': 0.60, 'TRY': 0.21, 'AED': 0.024, 'SAR': 0.024, 'BDT': 0.71},
    'INR': {'USD': 0.012, 'EUR': 0.011, 'GBP': 0.0095, 'JPY': 1.85, 'AUD': 0.018, 'CAD': 0.016, 'CHF': 0.011, 'CNY': 0.087, 'HKD': 0.094, 'NZD': 0.020, 'KRW': 16.30, 'SGD': 0.016, 'MXN': 0.20, 'BRL': 0.061, 'ZAR': 0.22, 'RUB': 1.11, 'TRY': 0.39, 'AED': 0.044, 'SAR': 0.045, 'BDT': 1.31},
    'AUD': {'USD': 0.66, 'EUR': 0.61, 'GBP': 0.52, 'JPY': 101.25, 'INR': 55.12, 'CAD': 0.90, 'CHF': 0.60, 'CNY': 4.76, 'HKD': 5.15, 'NZD': 1.10, 'KRW': 894.56, 'SGD': 0.89, 'MXN': 11.18, 'BRL': 3.37, 'ZAR': 12.32, 'RUB': 60.92, 'TRY': 21.25, 'AED': 2.42, 'SAR': 2.47, 'BDT': 72.15},
    'CAD': {'USD': 0.73, 'EUR': 0.68, 'GBP': 0.58, 'JPY': 112.45, 'INR': 61.20, 'AUD': 1.11, 'CHF': 0.67, 'CNY': 5.29, 'HKD': 5.72, 'NZD': 1.22, 'KRW': 993.78, 'SGD': 0.99, 'MXN': 12.42, 'BRL': 3.75, 'ZAR': 13.71, 'RUB': 67.78, 'TRY': 23.65, 'AED': 2.69, 'SAR': 2.74, 'BDT': 80.12},
    'CHF': {'USD': 1.10, 'EUR': 1.02, 'GBP': 0.87, 'JPY': 168.90, 'INR': 91.85, 'AUD': 1.67, 'CAD': 1.50, 'CNY': 7.95, 'HKD': 8.60, 'NZD': 1.83, 'KRW': 1490.23, 'SGD': 1.48, 'MXN': 18.56, 'BRL': 5.60, 'ZAR': 20.47, 'RUB': 101.25, 'TRY': 35.32, 'AED': 4.02, 'SAR': 4.10, 'BDT': 119.85},
    'CNY': {'USD': 0.14, 'EUR': 0.13, 'GBP': 0.11, 'JPY': 21.25, 'INR': 11.52, 'AUD': 0.21, 'CAD': 0.19, 'CHF': 0.13, 'HKD': 1.08, 'NZD': 0.23, 'KRW': 187.56, 'SGD': 0.19, 'MXN': 2.34, 'BRL': 0.71, 'ZAR': 2.59, 'RUB': 12.80, 'TRY': 4.47, 'AED': 0.51, 'SAR': 0.52, 'BDT': 15.18},
    'HKD': {'USD': 0.13, 'EUR': 0.12, 'GBP': 0.10, 'JPY': 19.60, 'INR': 10.65, 'AUD': 0.19, 'CAD': 0.17, 'CHF': 0.12, 'CNY': 0.93, 'NZD': 0.21, 'KRW': 173.45, 'SGD': 0.17, 'MXN': 2.17, 'BRL': 0.65, 'ZAR': 2.38, 'RUB': 11.78, 'TRY': 4.11, 'AED': 0.47, 'SAR': 0.48, 'BDT': 14.02},
    'NZD': {'USD': 0.60, 'EUR': 0.56, 'GBP': 0.47, 'JPY': 91.25, 'INR': 49.62, 'AUD': 0.91, 'CAD': 0.82, 'CHF': 0.55, 'CNY': 4.35, 'HKD': 4.71, 'KRW': 813.45, 'SGD': 0.81, 'MXN': 10.18, 'BRL': 3.07, 'ZAR': 11.22, 'RUB': 55.48, 'TRY': 19.36, 'AED': 2.20, 'SAR': 2.25, 'BDT': 65.78},
    'KRW': {'USD': 0.00074, 'EUR': 0.00068, 'GBP': 0.00058, 'JPY': 0.11, 'INR': 0.061, 'AUD': 0.0011, 'CAD': 0.0010, 'CHF': 0.00067, 'CNY': 0.0053, 'HKD': 0.0058, 'NZD': 0.0012, 'SGD': 0.00099, 'MXN': 0.012, 'BRL': 0.0037, 'ZAR': 0.014, 'RUB': 0.068, 'TRY': 0.024, 'AED': 0.0027, 'SAR': 0.0028, 'BDT': 0.081},
    'SGD': {'USD': 0.74, 'EUR': 0.69, 'GBP': 0.58, 'JPY': 113.45, 'INR': 61.72, 'AUD': 1.12, 'CAD': 1.01, 'CHF': 0.68, 'CNY': 5.35, 'HKD': 5.79, 'NZD': 1.23, 'KRW': 1008.90, 'MXN': 12.62, 'BRL': 3.81, 'ZAR': 13.92, 'RUB': 68.82, 'TRY': 24.01, 'AED': 2.73, 'SAR': 2.79, 'BDT': 81.52},
    'MXN': {'USD': 0.059, 'EUR': 0.055, 'GBP': 0.046, 'JPY': 8.99, 'INR': 4.89, 'AUD': 0.089, 'CAD': 0.081, 'CHF': 0.054, 'CNY': 0.43, 'HKD': 0.46, 'NZD': 0.098, 'KRW': 80.12, 'SGD': 0.079, 'BRL': 0.30, 'ZAR': 1.10, 'RUB': 5.45, 'TRY': 1.90, 'AED': 0.22, 'SAR': 0.22, 'BDT': 6.45},
    'BRL': {'USD': 0.20, 'EUR': 0.18, 'GBP': 0.15, 'JPY': 29.85, 'INR': 16.23, 'AUD': 0.30, 'CAD': 0.27, 'CHF': 0.18, 'CNY': 1.41, 'HKD': 1.53, 'NZD': 0.33, 'KRW': 270.45, 'SGD': 0.26, 'MXN': 3.33, 'ZAR': 3.65, 'RUB': 18.05, 'TRY': 6.30, 'AED': 0.72, 'SAR': 0.73, 'BDT': 21.40},
    'ZAR': {'USD': 0.053, 'EUR': 0.050, 'GBP': 0.042, 'JPY': 8.18, 'INR': 4.45, 'AUD': 0.081, 'CAD': 0.073, 'CHF': 0.049, 'CNY': 0.39, 'HKD': 0.42, 'NZD': 0.089, 'KRW': 72.78, 'SGD': 0.072, 'MXN': 0.91, 'BRL': 0.27, 'RUB': 4.95, 'TRY': 1.73, 'AED': 0.20, 'SAR': 0.20, 'BDT': 5.86},
    'RUB': {'USD': 0.011, 'EUR': 0.010, 'GBP': 0.0085, 'JPY': 1.65, 'INR': 0.90, 'AUD': 0.016, 'CAD': 0.015, 'CHF': 0.0099, 'CNY': 0.078, 'HKD': 0.085, 'NZD': 0.018, 'KRW': 14.72, 'SGD': 0.015, 'MXN': 0.18, 'BRL': 0.055, 'ZAR': 0.20, 'TRY': 0.35, 'AED': 0.040, 'SAR': 0.041, 'BDT': 1.19},
    'TRY': {'USD': 0.031, 'EUR': 0.029, 'GBP': 0.024, 'JPY': 4.72, 'INR': 2.57, 'AUD': 0.047, 'CAD': 0.042, 'CHF': 0.028, 'CNY': 0.22, 'HKD': 0.24, 'NZD': 0.052, 'KRW': 42.35, 'SGD': 0.042, 'MXN': 0.53, 'BRL': 0.16, 'ZAR': 0.58, 'RUB': 2.86, 'AED': 0.11, 'SAR': 0.12, 'BDT': 3.40},
    'AED': {'USD': 0.27, 'EUR': 0.25, 'GBP': 0.21, 'JPY': 41.72, 'INR': 22.69, 'AUD': 0.41, 'CAD': 0.37, 'CHF': 0.25, 'CNY': 1.96, 'HKD': 2.12, 'NZD': 0.45, 'KRW': 370.12, 'SGD': 0.37, 'MXN': 4.63, 'BRL': 1.40, 'ZAR': 5.11, 'RUB': 25.27, 'TRY': 8.82, 'SAR': 1.02, 'BDT': 29.85},
    'SAR': {'USD': 0.27, 'EUR': 0.25, 'GBP': 0.21, 'JPY': 40.85, 'INR': 22.22, 'AUD': 0.41, 'CAD': 0.37, 'CHF': 0.24, 'CNY': 1.93, 'HKD': 2.09, 'NZD': 0.44, 'KRW': 362.78, 'SGD': 0.36, 'MXN': 4.54, 'BRL': 1.37, 'ZAR': 5.01, 'RUB': 24.78, 'TRY': 8.65, 'AED': 0.98, 'BDT': 29.25},
    'BDT': {'USD': 0.0091, 'EUR': 0.0085, 'GBP': 0.0072, 'JPY': 1.40, 'INR': 0.76, 'AUD': 0.014, 'CAD': 0.012, 'CHF': 0.0083, 'CNY': 0.066, 'HKD': 0.071, 'NZD': 0.015, 'KRW': 12.35, 'SGD': 0.012, 'MXN': 0.16, 'BRL': 0.047, 'ZAR': 0.17, 'RUB': 0.84, 'TRY': 0.29, 'AED': 0.034, 'SAR': 0.034}
}
    
    if from_currency == to_currency:
        return amount

    try:
        rate = conversion_rates[from_currency][to_currency]
        return amount * rate
    except KeyError:
        return None

def convert_length(value, from_unit, to_unit):
    conversions = {
    'mm': 0.001, 'cm': 0.01, 'meter': 1.0, 'km': 1000.0, 'inch': 0.0254, 'ft': 0.3048, 'yard': 0.9144, 'mile': 1609.34, 'n-mile': 1852.0, 'µm': 0.000001, 'nm': 0.000000001
    }
    return value * conversions[from_unit] / conversions[to_unit]

def convert_time(value, from_unit, to_unit):
    conversions = {
    'ms': 0.001, 'second': 1.0, 'minute': 60.0, 'hour': 3600.0, 'day': 86400.0, 'week': 604800.0, 'month': 2629800.0, 'year': 31557600.0, 'decade': 315576000.0, 'century': 3155760000.0
    }
    return value * conversions[from_unit] / conversions[to_unit]

def convert_weight(value, from_unit, to_unit):
    conversions = {
    'µg': 0.000000001, 'mg': 0.000001, 'gram': 0.001, 'kg': 1.0, 'ton': 1000.0, 'ounce': 0.0283495,'pound': 0.453592, 'stone': 6.35029,        
    }
    return value * conversions[from_unit] / conversions[to_unit]

def convert_speed(value, from_unit, to_unit):
    conversions = {
    'm/s': 1.0, 'km/h': 0.277778, 'mile/h': 0.44704, 'ft/s': 0.3048,
    }
    return value * conversions[from_unit] / conversions[to_unit]

def convert_area(value, from_unit, to_unit):
    conversions = {
    'mm²': 0.000001, 'cm²': 0.0001, 'm²': 1.0, 'km²': 1000000.0, 'inch²': 0.00064516, 'ft²': 0.092903, 'yard²': 0.836127, 'acre': 4046.86, 'hectare': 10000.0, 'mile²': 2589988.11
}
    return value * conversions[from_unit] / conversions[to_unit]

def convert_volume(value, from_unit, to_unit):
    conversions = {
    'mm³': 0.000000001,
    'cm³': 0.000001,
    'm³': 1.0,
    'km³': 1000000000.0,
    'mL': 0.000001,
    'L': 0.001,
    'gallon': 0.00378541,
    'inch³': 0.0000163871,
    'ft³': 0.0283168,
}
    return value * conversions[from_unit] / conversions[to_unit]

def convert_temperature(value, from_unit, to_unit):
    if from_unit == '°C':
        if to_unit == '°F': return (value * 9/5) + 32
        elif to_unit == 'K': return value + 273.15
        else: return value
    elif from_unit == '°F':
        if to_unit == '°C': return (value - 32) * 5/9
        elif to_unit == 'K': return (value - 32) * 5/9 + 273.15
        else: return value
    elif from_unit == 'K':
        if to_unit == '°C': return value - 273.15
        elif to_unit == '°F': return (value - 273.15) * 9/5 + 32
        else: return value
    else: return value

def convert_pressure(value, from_unit, to_unit):
    conversions = {
    'Pa': 1.0, 'kPa': 1000.0, 'bar': 100000.0, 'atm': 101325.0, 'mmHg': 133.322, 'torr': 133.322
    }
    return value * conversions[from_unit] / conversions[to_unit]

def convert_force(value, from_unit, to_unit):
    conversions = {
    'N': 1.0, 'pound': 4.44822, 'dyne': 0.00001
    }
    return value * conversions[from_unit] / conversions[to_unit]

def convert_power(value, from_unit, to_unit):
    conversions = {
    'W': 1.0, 'kW': 1000.0, 'HP': 745.7,
    }
    return value * conversions[from_unit] / conversions[to_unit]

def convert_energy(value, from_unit, to_unit):
    conversions = {
    'J': 1.0, 'kJ': 1000.0, 'cal': 4.184, 'kcal': 4184.0, 'eV': 1.60218e-19,
    }
    return value * conversions[from_unit] / conversions[to_unit]

def convert_data(value, from_unit, to_unit):
    conversions = {
    'bit': 1,
    'byte': 8,
    'kilobit': 8000,
    'kilobyte': 8000,
    'megabyte': 8000000,
    'gigabyte': 8000000000,
    'terabyte': 8000000000000,
    }
    return value * conversions[from_unit] / conversions[to_unit]

def convert_frequency(value, from_unit, to_unit):
    conversions = {
    'Hz': 1.0, 'kHz': 1000.0, 'rpm': 1/60.0
    }
    return value * conversions[from_unit] / conversions[to_unit]

def convert_angle(value, from_unit, to_unit):
    conversions = {
    'degree': 1.0, 'radian': 180 / math.pi,
    }
    return value * conversions[from_unit] / conversions[to_unit]

def convert_fuel(value, from_unit, to_unit):
    if from_unit == 'mile/gal' and to_unit == 'liter/km':
        return 235.214583 / value
    elif from_unit == 'liter/km' and to_unit == 'mile/gal':
        return 235.214583 / value
    else:
        return value

def convert_torque(value, from_unit, to_unit):
    conversions = {
    'N-m': 1.0, 'lb-ft': 1.35582, 'lb-inch': 0.112985,
    }
    return value * conversions[from_unit] / conversions[to_unit]

def convert_illuminance(value, from_unit, to_unit):
    conversions = {
    'lux': 1.0, 'ft-cd': 10.7639, 'phot': 10000.0
    }
    return value * conversions[from_unit] / conversions[to_unit]

def convert_magnetic(value, from_unit, to_unit):
    conversions = {
    'A/m': 1.0, 'oersted': 79.5775, 'tesla': 795775.0
    }
    return value * conversions[from_unit] / conversions[to_unit]

def convert_radiation(value, from_unit, to_unit):
    conversions = {
    'bq': 1.0, 'curie': 3.7e10, 'rad': 0.01, 'roentgen': 0.01
    }
    return value * conversions[from_unit] / conversions[to_unit]

def convert_luminous(value, from_unit, to_unit):
    conversions = {
    'lumen': 1.0, 'cd-sr': 1.0
    }
    return value * conversions[from_unit] / conversions[to_unit]

def convert_sound(value, from_unit, to_unit):
    conversions = {
    'dB': 1.0, 'bel': 10.0,
    }
    return value * conversions[from_unit] / conversions[to_unit]

def convert_angular_velocity(value, from_unit, to_unit):
    conversions = {
    'rad/s': 1.0, 'deg/s': math.pi / 180, 'rpm': math.pi / 30
    }
    return value * conversions[from_unit] / conversions[to_unit]

def convert_charge(value, from_unit, to_unit):
    conversions = {
    'C': 1.0, 'mC': 0.001, 'µC': 0.000001, 'nC': 0.000000001,
    }
    return value * conversions[from_unit] / conversions[to_unit]

def convert_potential(value, from_unit, to_unit):
    conversions = {
    'V': 1.0, 'mV': 0.001, 'kV': 1000.0,
    }
    return value * conversions[from_unit] / conversions[to_unit]

def convert_resistance(value, from_unit, to_unit):
    conversions = {
    'ohm': 1.0, 'm-ohm': 0.001, 'k-ohm': 1000.0, 'M-ohm': 1000000.0,
    }
    return value * conversions[from_unit] / conversions[to_unit]

unit_categories = {
    'Length': ['mm', 'cm', 'meter', 'km', 'inch', 'ft', 'yard', 'mile', 'n-mile', 'µm', 'nm'],
    'Time': ['ms', 'second', 'minute', 'hour', 'day', 'week', 'month', 'year', 'decade', 'century'],
    'Weight': ['µg', 'mg', 'gram', 'kg', 'ton', 'ounce', 'pound', 'stone'],
    'Speed': ['m/s', 'km/h', 'mile/h', 'ft/s'],
    'Area': ['mm²', 'cm²', 'm²', 'km²', 'inch²', 'ft²', 'yard²', 'acre', 'hectare', 'mile²'],
    'Volume': ['cubic mm', 'cubic cm', 'cubic meter', 'cubic km', 'milliliter', 'liter', 'gallon', 'quart', 'pint', 'cup', 'fluid ounce', 'cubic inch', 'cubic foot', 'tablespoon', 'teaspoon'],
    'Temperature': ['°C', '°F', 'K'],
    'Pressure': ['Pa', 'kPa', 'bar', 'atm', 'mmHg', 'torr'],
    'Force': ['N', 'pound', 'dyne'],
    'Power': ['W', 'kW', 'HP'],
    'Energy': ['J', 'kJ', 'cal', 'kcal', 'eV'],
    'Data Storage': ['bit', 'byte', 'kilobit', 'kilobyte', 'megabyte', 'gigabyte', 'terabyte'],
    'Frequency': ['Hz', 'kHz', 'rpm'],
    'Angle': ['degree', 'radian'],
    'Fuel Efficiency': ['mile/gal', 'liter/km'],
    'Torque': ['N-m', 'lb-ft', 'lb-inch'],
    'Illuminance': ['lux', 'ft-cd', 'phot'],
    'Magnetic Field': ['A/m', 'oersted', 'tesla'],
    'Radiation': ['bq', 'curie', 'rad', 'roentgen'],
    'Luminous Flux': ['lumen', 'cd-sr'],
    'Sound': ['dB', 'bel'],
    'Angular Velocity': ['rad/s', 'deg/s', 'rpm'],
    'Electric Charge': ['C', 'mC', 'µC', 'nC'],
    'Electric Potential': ['V', 'mV', 'kV'],
    'Electric Resistance': ['ohm', 'm-ohm', 'k-ohm', 'M-ohm'],
    'Age Calculator': ['Birth Date'],
    'Currency': ['USD', 'EUR', 'GBP', 'JPY', 'INR', 'AUD', 'CAD', 'CHF', 'CNY', 'HKD', 'NZD', 'KRW', 'SGD', 'MXN', 'BRL', 'ZAR', 'RUB', 'TRY', 'AED', 'SAR', 'BDT']
}

conversion_functions = {
        'Length': convert_length,
        'Time': convert_time,
        'Weight': convert_weight,
        'Speed': convert_speed,
        'Area': convert_area,
        'Volume': convert_volume,
        'Temperature': convert_temperature,
        'Pressure': convert_pressure,
        'Force': convert_force,
        'Power': convert_power,
        'Energy': convert_energy,
        'Data Storage': convert_data,
        'Frequency': convert_frequency,
        'Angle': convert_angle,
        'Fuel Efficiency': convert_fuel,
        'Torque': convert_torque,
        'Illuminance': convert_illuminance,
        'Magnetic Field': convert_magnetic,
        'Radiation': convert_radiation,
        'Luminous Flux': convert_luminous,
        'Sound': convert_sound,
        'Angular Velocity': convert_angular_velocity,
        'Electric Charge': convert_charge,
        'Electric Potential': convert_potential,
        'Electric Resistance': convert_resistance
    }

@app.route('/')
def index():
    return render_template('index.html', categories=unit_categories.keys())

@app.route('/convert', methods=['POST'])
def convert():
    data = request.get_json()
    category = data['category']
    value = data['value']
    from_unit = data['from_unit']
    to_unit = data['to_unit']

    if category == 'Age Calculator':
        try:
            birth_date = datetime.strptime(value, '%Y-%m-%d').date()
            result = convert_age(birth_date)
            return jsonify({'result': f"{result} years"})
        except ValueError:
            return jsonify({'result': 'Invalid date format (YYYY-MM-DD)'})

    if category == 'Currency':
        try:
            amount = float(value)
            result = convert_currency(amount, from_unit, to_unit)
            if result is None:
                return jsonify({'result': 'Conversion not available'})
            return jsonify({'result': f"{round(result, 2)} {to_unit}"})
        except ValueError:
            return jsonify({'result': 'Invalid amount'})

    try:
        value = float(value)
    except ValueError:
        return jsonify({'result': 'Invalid value'})

    if category in conversion_functions:
        result = conversion_functions[category](value, from_unit, to_unit)
        if result is None:
            return jsonify({'result': 'Conversion error or unsupported units'})
        return jsonify({'result': f"{round(result, 8)} {to_unit}"})

    return jsonify({'result': 'Unsupported conversion category'})

@app.route('/get_units/<category>')
def get_units(category):
    return jsonify({'units': unit_categories.get(category, [])})

if __name__ == '__main__':
    app.run(debug=True)