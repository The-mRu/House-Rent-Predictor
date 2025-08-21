
from django.shortcuts import render
import pickle
import pandas as pd
import numpy as np
from django.http import JsonResponse

# Load model (already done)
with open('house_predictor/bd_house_model.pkl', 'rb') as f:
    model_data = pickle.load(f)

loaded_model = model_data['model']
loaded_features = model_data['feature_columns']

# Dropdown options (already defined)
def get_dropdown_options():
    type_options = ['Apartment', 'Duplex', 'Building']
    city_options = ['Dhaka', 'Chittagong']
    place_options = [
        'Bashundhara R-A', 'Khulshi', 'Uttara', 'Gulshan', 'Bayazid',
        'Khilgaon', 'Banani', 'Dhanmondi', 'Baridhara', 'Mirpur',
        'Rampura', 'Khilkhet', 'Mohammadpur', 'Kalabagan', 'other',
        'Mohakhali DOHS', '10 No. North Kattali Ward', 'Turag', 'Badda',
        'Shantinagar', 'Motijheel', 'Maghbazar', 'East Nasirabad',
        'Cantonment', 'Aftab Nagar', 'Dakshin Khan', 'Hazaribag',
        'Kazir Dewri', '9 No. North Pahartali Ward', 'Shiddheswari',
        'Malibagh', 'Adabor', 'Banasree', 'New Market', 'Ibrahimpur',
        'Baridhara DOHS', 'Lalbagh', 'Sholokbahar', 'Double Mooring',
        '15 No. Bagmoniram Ward', 'Panchlaish', 'Sutrapur', 'Eskaton',
        'Tejgaon', 'Lal Khan Bazaar', 'Muradpur', 'Halishahar',
        '4 No Chandgaon Ward', 'Shyamoli', '36 Goshail Danga Ward',
        '16 No. Chawk Bazaar Ward', 'Bakalia', 'Agargaon', 'Banani DOHS',
        'Nikunja', '22 No. Enayet Bazaar Ward', '11 No. South Kattali Ward',
        'Shegunbagicha', '7 No. West Sholoshohor Ward',
        'Jalalabad Housing Society', 'Patenga', 'Uttar Khan', 'Bashabo',
        '30 No. East Madarbari Ward', 'Shahjahanpur', '33 No. Firingee Bazaar Ward',
        'Others'
    ]
    beds_options = [1,2,3,4,5]
    bath_options = [1,2,3,4,5]
    return type_options, place_options, city_options, beds_options, bath_options

# Prediction function (already defined)
def predict_price_from_pkl(area_sqrt=None, beds=0, bath=0, type_='Apartment', place='other', city='Dhaka'):
    if area_sqrt is None:
        area_sqrt = 1000  # fallback

    x = pd.DataFrame(np.zeros((1, len(loaded_features))), columns=loaded_features)
    x['beds'] = beds
    x['bath'] = bath
    x['area_sqrt'] = area_sqrt

    for col_name, val in [('type', type_), ('place', place), ('city', city)]:
        feature = f"{col_name}_{val}"
        if feature in x.columns:
            x[feature] = 1

    return loaded_model.predict(x)[0]

# ---- Views ----
def predict_page(request):
    type_options, place_options, city_options, beds_options, bath_options = get_dropdown_options()
    context = {
        'type_options': type_options,
        'place_options': place_options,
        'city_options': city_options,
        'beds_options': beds_options,
        'bath_options': bath_options,
    }
    return render(request, 'house_predictor/predict.html', context)

def predict_result(request):
    # Get parameters from GET request
    beds = int(request.GET.get('beds', 0))
    bath = int(request.GET.get('bath', 0))
    type_ = request.GET.get('type_', 'Apartment')
    place = request.GET.get('place', 'other')
    city = request.GET.get('city', 'Dhaka')

    area_sqrt_str = request.GET.get('area_sqrt', '')
    if area_sqrt_str == '' or area_sqrt_str is None:
        area_sqrt = 1500  # default
    else:
        area_sqrt = float(area_sqrt_str)

    predicted_price = float(round(predict_price_from_pkl(
        area_sqrt=area_sqrt,
        beds=beds,
        bath=bath,
        type_=type_,
        place=place,
        city=city
    ), 2))
    
    predicted_price = int(predicted_price)  # Convert to integer for display


    context = {
        'beds': beds,
        'bath': bath,
        'type_': type_,
        'place': place,
        'city': city,
        'area_sqrt': area_sqrt,
        'predicted_price': predicted_price
    }

    return render(request, 'house_predictor/result.html', context)


# Home Page
def home_page(request):
    return render(request, 'house_predictor/home.html')

# About Page
def about_page(request):
    return render(request, 'house_predictor/about.html')

# Contact Page
def contact_page(request):
    return render(request, 'house_predictor/contact.html')