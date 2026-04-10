# Glucose classification rule engine
# Based on ADA (2026) exercise guidelines for Type 1 Diabetes
def classify_glucose(glucose_level):
    # Zone 1 - Treat Low
    if glucose_level < 70:
        return {
            'classification': 'Treat Low',
            'recommendation': 'Do not exercise. Treat with fast-acting carbohydrates immediately. Recheck glucose in 15 minutes.',
            'alert_caregiver': True,
            'zone': 1
        }
    # Zone 2 - Wait and Recheck
    elif glucose_level <= 89:
        return {
            'classification': 'Wait and Recheck',
            'recommendation': 'Give carbohydrates and wait 15 minutes before rechecking. Do not exercise yet.',
            'alert_caregiver': True,
            'zone': 2
        }
    # Zone 3 - Exercise with Caution
    elif glucose_level <= 125:
        return {
            'classification': 'Exercise with Caution',
            'recommendation': 'Have a snack available. Monitor closely, especially for long activity or downward CGM trend.',
            'alert_caregiver': False,
            'zone': 3
        }
    # Zone 4 - Ideal Starting Zone
    elif glucose_level <= 180:
        return {
            'classification': 'Ideal Starting Zone',
            'recommendation': 'Safe to exercise. No adjustment needed.',
            'alert_caregiver': False,
            'zone': 4
        }
    # Zone 5 - Usually Okay
    elif glucose_level <= 270:
        return {
            'classification': 'Usually Okay',
            'recommendation': 'Exercise is generally safe. Monitor during activity and recheck if symptoms appear.',
            'alert_caregiver': False,
            'zone': 5
        }
    # Zone 6 - Check Ketones First
    else:
        return {
            'classification': 'Check Ketones First',
            'recommendation': 'Do not exercise until ketones are checked. If ketones are elevated, do not exercise.',
            'alert_caregiver': True,
            'zone': 6
        }
    
def get_zone_color(zone):
    # Color coding for each zone
    colors = {
        1: 'red',       # Treat Low - danger
        2: 'orange',    # Wait and Recheck - warning
        3: 'yellow',    # Exercise with Caution - caution
        4: 'green',     # Ideal Starting Zone - safe
        5: 'blue',      # Usually Okay - monitor
        6: 'purple'     # Check Ketones First - danger
    }
    return colors.get(zone, 'gray')

if __name__ == '__main__':
    # Test all six zones and boundary values
    test_readings = [65, 70, 89, 90, 125, 126, 180, 181, 270, 271]

    print("Glucose Rule Engine Test")
    print("=" * 50)

    for glucose in test_readings:
        result = classify_glucose(glucose)
        color = get_zone_color(result['zone'])
        print(f"\nGlucose: {glucose} mg/dL")
        print(f"  Zone          : {result['zone']} ({color})")
        print(f"  Classification: {result['classification']}")
        print(f"  Recommendation: {result['recommendation']}")
        print(f"  Alert Caregiver: {result['alert_caregiver']}")