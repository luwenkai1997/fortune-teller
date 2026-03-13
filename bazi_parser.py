# -*- coding: utf-8 -*-
"""
八字解析模块
使用 sxtwl 库进行精确的八字计算
"""

import sxtwl
from typing import Dict, List

# ============ 常量定义 ============

TIANGAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
DIZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

TIANGAN_WUXING = {
    '甲': '木', '乙': '木',
    '丙': '火', '丁': '火',
    '戊': '土', '己': '土',
    '庚': '金', '辛': '金',
    '壬': '水', '癸': '水'
}

DIZHI_WUXING = {
    '子': '水', '丑': '土', '寅': '木', '卯': '木',
    '辰': '土', '巳': '火', '午': '火', '未': '土',
    '申': '金', '酉': '金', '戌': '土', '亥': '水'
}

DIZHI_CANGGAN = {
    '子': ['癸'],
    '丑': ['己', '癸', '辛'],
    '寅': ['甲', '丙', '戊'],
    '卯': ['乙'],
    '辰': ['戊', '乙', '癸'],
    '巳': ['丙', '庚', '戊'],
    '午': ['丁', '己'],
    '未': ['己', '丁', '乙'],
    '申': ['庚', '壬', '戊'],
    '酉': ['辛'],
    '戌': ['戊', '辛', '丁'],
    '亥': ['壬', '甲']
}


def get_bazi(year: int, month: int, day: int, hour: int, minute: int = 0) -> Dict:
    """使用 sxtwl 库获取准确八字"""
    # 创建 sxtwl 日期对象
    day_obj = sxtwl.fromSolar(year, month, day)
    
    # 获取四柱
    year_gz = day_obj.getYearGZ()
    month_gz = day_obj.getMonthGZ()
    day_gz = day_obj.getDayGZ()
    hour_gz = day_obj.getHourGZ(hour)
    
    bazi = {
        'year': TIANGAN[year_gz.tg] + DIZHI[year_gz.dz],
        'month': TIANGAN[month_gz.tg] + DIZHI[month_gz.dz],
        'day': TIANGAN[day_gz.tg] + DIZHI[day_gz.dz],
        'hour': TIANGAN[hour_gz.tg] + DIZHI[hour_gz.dz],
        'day_zhu': DIZHI[day_gz.dz]
    }
    
    return bazi


def calculate_wuxing_strength(bazi: Dict) -> Dict:
    """计算五行强度"""
    wuxing_count = {'木': 0, '火': 0, '土': 0, '金': 0, '水': 0}
    
    for column in ['year', 'month', 'day', 'hour']:
        ganzhi = bazi[column]
        gan = ganzhi[0]
        zhi = ganzhi[1]
        
        wuxing_count[TIANGAN_WUXING[gan]] += 1
        wuxing_count[DIZHI_WUXING[zhi]] += 1
        
        for canggan in DIZHI_CANGGAN[zhi]:
            wuxing_count[TIANGAN_WUXING[canggan]] += 0.5
    
    return wuxing_count


def calculate_shishen(bazi: Dict) -> Dict:
    """计算十神"""
    day_gan = bazi['day'][0]
    day_gan_wuxing = TIANGAN_WUXING[day_gan]
    
    wuxing_relation = {
        '木': {'木': '比肩', '火': '食神', '土': '财星', '金': '官杀', '水': '印星'},
        '火': {'木': '印星', '火': '比肩', '土': '食神', '金': '财星', '水': '官杀'},
        '土': {'木': '官杀', '火': '印星', '土': '比肩', '金': '食神', '水': '财星'},
        '金': {'木': '财星', '火': '官杀', '土': '印星', '金': '比肩', '水': '食神'},
        '水': {'木': '食神', '火': '财星', '土': '官杀', '金': '印星', '水': '比肩'}
    }
    
    shishen = {}
    for column in ['year', 'month', 'day', 'hour']:
        ganzhi = bazi[column]
        gan = ganzhi[0]
        gan_wuxing = TIANGAN_WUXING[gan]
        shishen_name = wuxing_relation[day_gan_wuxing][gan_wuxing]
        shishen[column] = f"{gan}（{shishen_name}）"
    
    return shishen


def determine_xiyongshen(bazi: Dict, wuxing_strength: Dict) -> tuple:
    """判断喜用神"""
    day_gan = bazi['day'][0]
    day_gan_wuxing = TIANGAN_WUXING[day_gan]
    
    day_energy = wuxing_strength[day_gan_wuxing]
    total_energy = sum(wuxing_strength.values())
    ratio = day_energy / total_energy if total_energy > 0 else 0
    
    if ratio >= 0.4 or day_energy >= 3:
        mingshu = '身强'
        opposite = {'木': '金', '火': '水', '土': '木', '金': '火', '水': '土'}
        generating = {'木': '火', '火': '土', '土': '金', '金': '水', '水': '木'}
        xiyong = [opposite[day_gan_wuxing], generating[day_gan_wuxing], '财星']
    else:
        mingshu = '身弱'
        generating = {'木': '水', '火': '木', '土': '火', '金': '土', '水': '金'}
        same = day_gan_wuxing
        xiyong = [generating[day_gan_wuxing], same]
    
    return ','.join(xiyong), mingshu


def calculate_dayun(bazi: Dict, birth_year: int) -> List[Dict]:
    """计算大运（20-60岁，4个大运）"""
    day_gan = bazi['day'][0]
    day_zhi = bazi['day_zhu']
    
    is_yang = TIANGAN.index(day_gan) % 2 == 0
    day_zhi_index = DIZHI.index(day_zhi)
    
    dayun = []
    for i in range(4):
        age_start = 20 + i * 10
        if is_yang:
            zhi_index = (day_zhi_index + i + 1) % 12
            gan_index = (TIANGAN.index(day_gan) + i + 1) % 10
        else:
            zhi_index = (day_zhi_index - i - 1) % 12
            gan_index = (TIANGAN.index(day_gan) - i - 1) % 10
        
        ganzhi = TIANGAN[gan_index] + DIZHI[zhi_index]
        
        dayun.append({
            'age': age_start,
            'start': str(birth_year + age_start),
            'end': str(birth_year + age_start + 9),
            'ganzhi': ganzhi
        })
    
    return dayun


def calculate_liunian(birth_year: int) -> List[Dict]:
    """计算流年（最近3年）"""
    import datetime
    current_year = datetime.datetime.now().year
    
    liunian = []
    for i in range(3):
        year = current_year - i
        day_obj = sxtwl.fromSolar(year, 1, 1)
        year_gz = day_obj.getYearGZ()
        ganzhi = TIANGAN[year_gz.tg] + DIZHI[year_gz.dz]
        liunian.insert(0, {'year': str(year), 'ganzhi': ganzhi})
    
    return liunian


def analyze_bazi(birth_date: str, birth_time: str, gender: str, question_type: str) -> Dict:
    """完整的八字分析"""
    import datetime
    
    date_part = datetime.datetime.strptime(birth_date, '%Y-%m-%d')
    time_part = datetime.datetime.strptime(birth_time, '%H:%M')
    
    birth_year = date_part.year
    
    # 使用 sxtwl 获取准确八字
    bazi = get_bazi(
        date_part.year, 
        date_part.month, 
        date_part.day, 
        time_part.hour,
        time_part.minute
    )
    
    wuxing_strength = calculate_wuxing_strength(bazi)
    shishen = calculate_shishen(bazi)
    xiyongshen, mingshu = determine_xiyongshen(bazi, wuxing_strength)
    dayun = calculate_dayun(bazi, birth_year)
    liunian = calculate_liunian(birth_year)
    
    return {
        'bazi': bazi,
        'wuxing_strength': wuxing_strength,
        'shishen': shishen,
        'xiyongshen': xiyongshen,
        'mingshu': mingshu,
        'dayun': dayun,
        'liunian': liunian
    }


if __name__ == '__main__':
    # 测试：1997年12月15日19:31
    result = analyze_bazi('1997-12-15', '19:31', '男', '事业')
    
    print("=== 测试结果 ===")
    print("八字:", result['bazi'])
    print("五行强度:", result['wuxing_strength'])
    print("十神:", result['shishen'])
    print("喜用神:", result['xiyongshen'])
    print("命主:", result['mingshu'])
    print("大运:", result['dayun'])
    print("流年:", result['liunian'])