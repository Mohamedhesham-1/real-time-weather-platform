from datetime import datetime


# ==============================
# SVG Drawings
# ==============================

def _svg_tshirt_shorts(color1="#4A90D9", color2="#5B5EA6"):
    return f"""
    <svg viewBox="0 0 200 250" xmlns="http://www.w3.org/2000/svg">
      <!-- T-Shirt -->
      <polygon points="60,30 30,60 50,65 50,130 150,130 150,65 170,60 140,30 120,50 80,50" fill="{color1}" stroke="#333" stroke-width="2"/>
      <!-- Shorts -->
      <rect x="55" y="135" width="90" height="60" rx="5" fill="{color2}" stroke="#333" stroke-width="2"/>
      <line x1="100" y1="135" x2="100" y2="195" stroke="#333" stroke-width="2"/>
      <!-- Shoes -->
      <ellipse cx="75" cy="215" rx="25" ry="10" fill="#333"/>
      <ellipse cx="125" cy="215" rx="25" ry="10" fill="#333"/>
    </svg>"""

def _svg_tshirt_pants(color1="#4A90D9", color2="#2C3E50"):
    return f"""
    <svg viewBox="0 0 200 280" xmlns="http://www.w3.org/2000/svg">
      <!-- T-Shirt -->
      <polygon points="60,30 30,60 50,65 50,130 150,130 150,65 170,60 140,30 120,50 80,50" fill="{color1}" stroke="#333" stroke-width="2"/>
      <!-- Pants -->
      <rect x="55" y="135" width="90" height="100" rx="5" fill="{color2}" stroke="#333" stroke-width="2"/>
      <line x1="100" y1="135" x2="100" y2="235" stroke="#333" stroke-width="2"/>
      <!-- Shoes -->
      <ellipse cx="75" cy="245" rx="25" ry="10" fill="#333"/>
      <ellipse cx="125" cy="245" rx="25" ry="10" fill="#333"/>
    </svg>"""

def _svg_hoodie_pants(color1="#E67E22", color2="#2C3E50"):
    return f"""
    <svg viewBox="0 0 200 280" xmlns="http://www.w3.org/2000/svg">
      <!-- Hoodie -->
      <polygon points="60,30 25,65 50,70 50,140 150,140 150,70 175,65 140,30 120,55 80,55" fill="{color1}" stroke="#333" stroke-width="2"/>
      <!-- Hood -->
      <path d="M80,30 Q100,10 120,30 Q110,55 100,55 Q90,55 80,30" fill="{color1}" stroke="#333" stroke-width="2"/>
      <!-- Pocket -->
      <rect x="75" y="100" width="50" height="25" rx="5" fill="{color1}" stroke="#333" stroke-width="1.5"/>
      <!-- Pants -->
      <rect x="55" y="145" width="90" height="95" rx="5" fill="{color2}" stroke="#333" stroke-width="2"/>
      <line x1="100" y1="145" x2="100" y2="240" stroke="#333" stroke-width="2"/>
      <!-- Shoes -->
      <ellipse cx="75" cy="250" rx="25" ry="10" fill="#333"/>
      <ellipse cx="125" cy="250" rx="25" ry="10" fill="#333"/>
    </svg>"""

def _svg_jacket_pants(color1="#C0392B", color2="#2C3E50", scarf=False):
    scarf_svg = """<path d="M75,35 Q100,25 125,35 Q120,55 100,60 Q80,55 75,35" fill="#E74C3C" stroke="#333" stroke-width="1.5"/>""" if scarf else ""
    return f"""
    <svg viewBox="0 0 200 290" xmlns="http://www.w3.org/2000/svg">
      <!-- Jacket -->
      <polygon points="60,35 25,70 50,75 50,150 150,150 150,75 175,70 140,35 115,60 85,60" fill="{color1}" stroke="#333" stroke-width="2"/>
      <!-- Jacket Zipper -->
      <line x1="100" y1="60" x2="100" y2="150" stroke="#333" stroke-width="2"/>
      <!-- Collar -->
      <polygon points="85,35 100,60 115,35 100,45" fill="#922B21" stroke="#333" stroke-width="1"/>
      {scarf_svg}
      <!-- Pants -->
      <rect x="55" y="155" width="90" height="95" rx="5" fill="{color2}" stroke="#333" stroke-width="2"/>
      <line x1="100" y1="155" x2="100" y2="250" stroke="#333" stroke-width="2"/>
      <!-- Boots -->
      <rect x="52" y="248" width="45" height="20" rx="5" fill="#4A4A4A" stroke="#333" stroke-width="2"/>
      <rect x="103" y="248" width="45" height="20" rx="5" fill="#4A4A4A" stroke="#333" stroke-width="2"/>
    </svg>"""

def _svg_heavy_coat(color1="#1A252F", color2="#2C3E50"):
    return f"""
    <svg viewBox="0 0 200 300" xmlns="http://www.w3.org/2000/svg">
      <!-- Heavy Coat -->
      <polygon points="55,30 20,75 48,80 48,170 152,170 152,80 180,75 145,30 118,62 82,62" fill="{color1}" stroke="#333" stroke-width="2"/>
      <!-- Coat Buttons -->
      <circle cx="100" cy="90" r="4" fill="#BDC3C7"/>
      <circle cx="100" cy="110" r="4" fill="#BDC3C7"/>
      <circle cx="100" cy="130" r="4" fill="#BDC3C7"/>
      <circle cx="100" cy="150" r="4" fill="#BDC3C7"/>
      <!-- Collar -->
      <polygon points="82,30 100,65 118,30 100,48" fill="#17202A" stroke="#333" stroke-width="1.5"/>
      <!-- Scarf -->
      <path d="M72,32 Q100,20 128,32 Q122,58 100,63 Q78,58 72,32" fill="#E74C3C" stroke="#333" stroke-width="1.5"/>
      <!-- Pants -->
      <rect x="53" y="175" width="94" height="85" rx="5" fill="{color2}" stroke="#333" stroke-width="2"/>
      <line x1="100" y1="175" x2="100" y2="260" stroke="#333" stroke-width="2"/>
      <!-- Boots -->
      <rect x="50" y="258" width="45" height="22" rx="5" fill="#2C2C2C" stroke="#333" stroke-width="2"/>
      <rect x="105" y="258" width="45" height="22" rx="5" fill="#2C2C2C" stroke="#333" stroke-width="2"/>
    </svg>"""

def _svg_formal(color1="#2C3E50", color2="#1A252F"):
    return f"""
    <svg viewBox="0 0 200 290" xmlns="http://www.w3.org/2000/svg">
      <!-- Suit Jacket -->
      <polygon points="60,35 25,70 50,75 50,155 150,155 150,75 175,70 140,35 115,62 85,62" fill="{color1}" stroke="#333" stroke-width="2"/>
      <!-- Shirt -->
      <polygon points="85,35 100,65 115,35 115,155 85,155" fill="white" stroke="#333" stroke-width="1"/>
      <!-- Tie -->
      <polygon points="96,50 104,50 102,120 100,125 98,120" fill="#C0392B" stroke="#333" stroke-width="1"/>
      <!-- Lapels -->
      <polygon points="85,35 100,65 50,75 50,90" fill="{color1}" stroke="#333" stroke-width="1"/>
      <polygon points="115,35 100,65 150,75 150,90" fill="{color1}" stroke="#333" stroke-width="1"/>
      <!-- Pants -->
      <rect x="55" y="160" width="90" height="90" rx="5" fill="{color2}" stroke="#333" stroke-width="2"/>
      <line x1="100" y1="160" x2="100" y2="250" stroke="#333" stroke-width="2"/>
      <!-- Formal Shoes -->
      <ellipse cx="75" cy="262" rx="27" ry="10" fill="#1A1A1A" stroke="#333" stroke-width="1.5"/>
      <ellipse cx="125" cy="262" rx="27" ry="10" fill="#1A1A1A" stroke="#333" stroke-width="1.5"/>
    </svg>"""

def _svg_sportswear(color1="#27AE60", color2="#1A252F"):
    return f"""
    <svg viewBox="0 0 200 270" xmlns="http://www.w3.org/2000/svg">
      <!-- Sports Top -->
      <polygon points="65,30 35,60 52,65 52,125 148,125 148,65 165,60 135,30 118,48 82,48" fill="{color1}" stroke="#333" stroke-width="2"/>
      <!-- Sports Stripes -->
      <line x1="52" y1="80" x2="148" y2="80" stroke="white" stroke-width="3" opacity="0.5"/>
      <!-- Sports Pants -->
      <rect x="55" y="130" width="90" height="95" rx="8" fill="{color2}" stroke="#333" stroke-width="2"/>
      <line x1="100" y1="130" x2="100" y2="225" stroke="#333" stroke-width="2"/>
      <!-- Stripe on pants -->
      <line x1="58" y1="140" x2="58" y2="220" stroke="{color1}" stroke-width="4"/>
      <line x1="142" y1="140" x2="142" y2="220" stroke="{color1}" stroke-width="4"/>
      <!-- Sneakers -->
      <ellipse cx="75" cy="238" rx="26" ry="11" fill="white" stroke="#333" stroke-width="2"/>
      <ellipse cx="125" cy="238" rx="26" ry="11" fill="white" stroke="#333" stroke-width="2"/>
    </svg>"""


# ==============================
# Core Logic
# ==============================

def _get_time_of_day(sunrise: datetime, sunset: datetime) -> str:
    now = datetime.now()
    sunrise_t = sunrise.replace(tzinfo=None) if sunrise.tzinfo else sunrise
    sunset_t = sunset.replace(tzinfo=None) if sunset.tzinfo else sunset

    hour = now.hour
    sunrise_hour = sunrise_t.hour
    sunset_hour = sunset_t.hour

    if hour < sunrise_hour + 1:
        return "فجر"
    elif hour < 12:
        return "صبح"
    elif hour < 15:
        return "ضهر"
    elif hour < sunset_hour:
        return "عصر"
    elif hour < sunset_hour + 2:
        return "مغرب"
    else:
        return "ليل"


def _temp_level(temp, feels_like):
    effective = (temp + feels_like) / 2
    if effective < 10:
        return "شتاء قوي"
    elif effective < 15:
        return "برد"
    elif effective < 20:
        return "لطيف برد"
    elif effective < 25:
        return "معتدل"
    elif effective < 30:
        return "دافي"
    else:
        return "حر"


def _humidity_note(humidity):
    if humidity > 85:
        return "رطوبة خانقة - القطن الخالص مش مناسب خالص"
    elif humidity > 70:
        return "رطوبة عالية - اختار قماش خفيف مش قطن خالص"
    elif humidity < 30:
        return "جو جاف - استخدم كريم مرطب"
    return None


def _wind_note(wind_speed):
    if wind_speed > 20:
        return "رياح شديدة جداً - الجاكيت ضروري ومحتاج تتحاشى الخروج"
    elif wind_speed > 10:
        return "رياح قوية - لازم جاكيت مقاوم للرياح"
    elif wind_speed > 5:
        return "فيه رياح - خد بالك"
    return None


def _rain_note(weather_desc):
    desc = weather_desc.lower()
    if any(w in desc for w in ["thunderstorm", "heavy rain", "heavy shower"]):
        return "عواصف أو مطر غزير - شمسية كبيرة + جزمة مطر"
    elif any(w in desc for w in ["rain", "drizzle", "shower"]):
        return "محتمل مطر - خد شمسية صغيرة أو جاكيت waterproof"
    elif "cloud" in desc:
        return "غيوم - ممكن يمطر، يستحسن تاخد شمسية"
    return None


def _get_outfit_by_occasion_gender_temp(occasion, gender, temp_level, wind_speed, weather_desc):
    desc = weather_desc.lower()
    is_rainy = any(w in desc for w in ["rain", "drizzle", "shower", "thunderstorm"])
    is_windy = wind_speed > 10

    if occasion == "رياضة":
        if temp_level in ["شتاء قوي", "برد"]:
            return {
                "tops": ["تيشيرت رياضي تيرمال", "هودي رياضي فوقيه"],
                "bottoms": ["تايتس رياضي", "بنطلون رياضي فوق التايتس"],
                "shoes": "سنيكرز رياضي مغلق",
                "accessories": ["جوانتي رياضي", "بند راس رياضي"],
                "svg": _svg_sportswear("#2980B9", "#1A252F")
            }
        elif temp_level in ["لطيف برد", "معتدل"]:
            return {
                "tops": ["تيشيرت رياضي"],
                "bottoms": ["شورت رياضي" if temp_level == "معتدل" else "بنطلون رياضي"],
                "shoes": "سنيكرز رياضي خفيف",
                "accessories": [],
                "svg": _svg_sportswear("#27AE60", "#2C3E50")
            }
        else:
            return {
                "tops": ["تيشيرت رياضي خفيف جداً"],
                "bottoms": ["شورت رياضي خفيف"],
                "shoes": "سنيكرز خفيف أو شبشب رياضي",
                "accessories": ["كاب عشان الشمس"],
                "svg": _svg_sportswear("#E67E22", "#1A252F")
            }

    if occasion == "شغل":
        if temp_level in ["شتاء قوي", "برد"]:
            return {
                "tops": ["قميص فورمال", "بدلة أو جاكيت سوت فوقيه", "كوت لو برا"],
                "bottoms": ["بنطلون فورمال"],
                "shoes": "جزمة جلد أو حذاء فورمال",
                "accessories": ["كرافت أو تاي", "سكارف لو برا"],
                "svg": _svg_formal()
            }
        elif temp_level in ["لطيف برد", "معتدل"]:
            return {
                "tops": ["قميص سمارت كاجوال", "بليزر خفيف"],
                "bottoms": ["بنطلون chinos أو فورمال"],
                "shoes": "حذاء جلد خفيف أو لوفر",
                "accessories": ["ساعة", "حزام جلد"],
                "svg": _svg_formal("#34495E", "#2C3E50")
            }
        else:
            return {
                "tops": ["قميص قطن خفيف بكم" if gender == "رجالي" else "بلوزة خفيفة"],
                "bottoms": ["بنطلون chinos فاتح اللون"],
                "shoes": "لوفر أو حذاء خفيف",
                "accessories": ["ساعة"],
                "svg": _svg_formal("#5D6D7E", "#1A252F")
            }

    # كاجوال أو خروج
    if temp_level == "شتاء قوي":
        return {
            "tops": ["تيشيرت تيرمال", "سويتشيرت تقيل فوقيه", "كوت أو باركا فوقيهم"],
            "bottoms": ["جينز سميك أو بنطلون صوف"],
            "shoes": "بوت جلد أو حذاء مغلق تقيل",
            "accessories": ["سكارف صوف", "طاقية", "جوانتي"],
            "svg": _svg_heavy_coat()
        }
    elif temp_level == "برد":
        return {
            "tops": ["تيشيرت", "هودي أو سويتشيرت فوقيه", "جاكيت مقاوم للرياح" if is_windy else ""],
            "bottoms": ["جينز عادي"],
            "shoes": "سنيكرز مغلق أو بوت خفيف",
            "accessories": ["سكارف خفيف", "شمسية" if is_rainy else ""],
            "svg": _svg_jacket_pants(scarf=True)
        }
    elif temp_level == "لطيف برد":
        return {
            "tops": ["تيشيرت", "هودي أو قميص فوقيه"],
            "bottoms": ["جينز"],
            "shoes": "سنيكرز",
            "accessories": ["شمسية" if is_rainy else ""],
            "svg": _svg_hoodie_pants()
        }
    elif temp_level == "معتدل":
        return {
            "tops": ["تيشيرت خفيف" if gender == "رجالي" else "تيشيرت أو بلوزة خفيفة"],
            "bottoms": ["جينز أو chinos"],
            "shoes": "سنيكرز أو كوتشي",
            "accessories": ["شمسية" if is_rainy else ""],
            "svg": _svg_tshirt_pants()
        }
    elif temp_level == "دافي":
        return {
            "tops": ["تيشيرت خفيف"],
            "bottoms": ["شورت أو جينز خفيف"],
            "shoes": "سنيكرز خفيف أو شبشب",
            "accessories": ["نظارة شمس", "كاب"],
            "svg": _svg_tshirt_shorts()
        }
    else:  # حر
        return {
            "tops": ["تيشيرت قطن خفيف جداً" if gender == "رجالي" else "تيشيرت أو فستان صيفي خفيف"],
            "bottoms": ["شورت خفيف"],
            "shoes": "شبشب أو صندل",
            "accessories": ["نظارة شمس", "كاب أو قبعة", "واقي شمس ضروري"],
            "svg": _svg_tshirt_shorts("#FF6B6B", "#4ECDC4")
        }


# ==============================
# Main Function
# ==============================

def get_outfit_recommendation(
    temp: float,
    feels_like: float,
    humidity: int,
    wind_speed: float,
    weather_desc: str,
    sunrise: datetime,
    sunset: datetime,
    gender: str = "رجالي",
    occasion: str = "كاجوال"
) -> dict:
    """
    بتاخد بيانات الطقس وترجع اقتراح الملابس الكامل.

    Parameters:
        temp         : درجة الحرارة الفعلية
        feels_like   : درجة الحرارة المحسوسة
        humidity     : الرطوبة %
        wind_speed   : سرعة الرياح m/s
        weather_desc : وصف الطقس من API
        sunrise      : وقت الشروق
        sunset       : وقت الغروب
        gender       : رجالي / حريمي
        occasion     : كاجوال / شغل / رياضة / خروج

    Returns:
        dict فيه كل تفاصيل الاقتراح + SVG
    """

    time_of_day = _get_time_of_day(sunrise, sunset)
    temp_level = _temp_level(temp, feels_like)
    humidity_note = _humidity_note(humidity)
    wind_note = _wind_note(wind_speed)
    rain_note = _rain_note(weather_desc)

    outfit = _get_outfit_by_occasion_gender_temp(
        occasion, gender, temp_level, wind_speed, weather_desc
    )

    # تنظيف الـ accessories من القيم الفاضية
    outfit["accessories"] = [a for a in outfit.get("accessories", []) if a]
    outfit["tops"] = [t for t in outfit.get("tops", []) if t]

    warnings = []
    if humidity_note:
        warnings.append(humidity_note)
    if wind_note:
        warnings.append(wind_note)
    if rain_note:
        warnings.append(rain_note)

    return {
        "temp": temp,
        "feels_like": feels_like,
        "humidity": humidity,
        "wind_speed": wind_speed,
        "weather_desc": weather_desc,
        "time_of_day": time_of_day,
        "temp_level": temp_level,
        "gender": gender,
        "occasion": occasion,
        "outfit": outfit,
        "warnings": warnings,
        "svg": outfit.get("svg", "")
    }