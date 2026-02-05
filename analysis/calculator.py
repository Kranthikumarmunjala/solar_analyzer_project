def calculate_score(site, weights):
    # Solar Score
    if site.solar_irradiance_kwh >= 5.5:
        solar_score = 100.0
    elif site.solar_irradiance_kwh < 3.0:
        solar_score = 0.0
    else:
        solar_score = ((float(site.solar_irradiance_kwh) - 3.0) / 2.5) * 100

    # Area Score
    if site.area_sqm >= 50000:
        area_score = 100.0
    elif site.area_sqm < 5000:
        area_score = 0.0
    else:
        area_score = ((site.area_sqm - 5000) / 45000) * 100

    # Grid Distance Score
    if site.grid_distance_km <= 1:
        grid_score = 100.0
    elif site.grid_distance_km >= 20:
        grid_score = 0.0
    else:
        grid_score = 100 - ((float(site.grid_distance_km) - 1) / 19) * 100

    # Slope Score
    slope = float(site.slope_degrees)
    if slope <= 5:
        slope_score = 100.0
    elif slope > 20:
        slope_score = 0.0
    elif slope <= 15:
        slope_score = 100 - ((slope - 5) / 10) * 50
    else:
        slope_score = 50 - ((slope - 15) / 5) * 50

    # Infrastructure Score
    if site.road_distance_km <= 0.5:
        infra_score = 100.0
    elif site.road_distance_km >= 5:
        infra_score = 0.0
    else:
        infra_score = 100 - ((float(site.road_distance_km) - 0.5) / 4.5) * 100

    # Total
    total = (
        solar_score * weights['solar'] +
        area_score * weights['area'] +
        grid_score * weights['grid'] +
        slope_score * weights['slope'] +
        infra_score * weights['infrastructure']
    )

    return {
        'total': round(total, 2),
        'breakdown': {
            'solar': round(solar_score, 2),
            'area': round(area_score, 2),
            'grid': round(grid_score, 2),
            'slope': round(slope_score, 2),
            'infrastructure': round(infra_score, 2)
        }
    }