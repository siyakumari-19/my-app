from flask import Flask, request, render_template_string, jsonify
import math

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Electrical Systems Calculator</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f9; color: #333; margin: 0; padding: 0; }
        .header-menu { background-color: #007BFF; color: white; padding: 10px 0; text-align: center; }
        .header-menu a { color: white; text-decoration: none; padding: 10px 15px; margin: 0 5px; font-weight: bold; transition: background-color 0.3s; border-radius: 5px; }
        .header-menu a:hover { background-color: #0056b3; }
        .container { max-width: 900px; margin: 30px auto; background: #ffffff; padding: 30px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1); border-radius: 12px; }
        .calc-section { display: none; }
        .calc-section.active { display: block; }
        h1, h2 { color: #007BFF; text-align: center; }
        .calc-card { border: 1px solid #e0e0e0; padding: 20px; border-radius: 8px; margin-top: 20px; }
        .input-row { display: flex; align-items: center; justify-content: space-between; margin: 10px 0; }
        .input-row label { flex: 1; text-align: left; margin-right: 10px; font-weight: 600; }
        .input-row input { flex: 2; padding: 8px; border: 1px solid #ccc; border-radius: 4px; text-align: right; }
        .input-row .value-display { flex: 2; text-align: right; font-weight: bold; padding: 8px; border: 1px solid transparent; border-radius: 4px; }
        button { width: 100%; padding: 12px; background-color: #007BFF; color: white; border: none; border-radius: 6px; font-size: 16px; cursor: pointer; margin-top: 20px; transition: background-color 0.3s; }
        button:hover { background-color: #0056b3; }
        .result-box { margin-top: 20px; padding: 15px; border-radius: 6px; font-weight: bold; }
        .result-box.success { background-color: #e2f0e2; border: 1px solid #4CAF50; color: #4CAF50; }
        .result-box.error { background-color: #f8d7da; border: 1px solid #dc3545; color: #dc3545; }
    </style>
</head>
<body>
    <div class="header-menu">
        <a href="#common_formula" onclick="showCalculator('common_formula')">Common Formula</a>
        <a href="#three_phase_power" onclick="showCalculator('three_phase_power')">3 Phase Power</a>
        <a href="#delta_connection" onclick="showCalculator('delta_connection')">Delta Connection</a>
        <a href="#star_connection" onclick="showCalculator('star_connection')">Star Connection</a>
        <a href="#power_factor" onclick="showCalculator('power_factor')">Power Factor</a>
        <a href="#reactive_power" onclick="showCalculator('reactive_power')">Reactive Power</a>
        <a href="#kva_to_kw" onclick="showCalculator('kva_to_kw')">KVA to kW</a>
        <a href="#three_to_single_phase" onclick="showCalculator('three_to_single_phase')">3 to 1 Phase</a>
    </div>

    <div class="container">
        <div id="common_formula" class="calc-section">
            <h2>Common Formula Calculations</h2>
            <div class="calc-card">
                <form onsubmit="calculate(event, 'common_formula')">
                    <div class="input-row"><label>Resistance =</label><input type="text" name="Resistance" id="Resistance_common"></div>
                    <div class="input-row"><label>Current =</label><input type="text" name="Current" id="Current_common"></div>
                    <div class="input-row"><label>Voltage =</label><input type="text" name="Voltage" id="Voltage_common"></div>
                    <button type="submit">Calculate</button>
                    <div class="result-box" id="result-common_formula"></div>
                </form>
            </div>
        </div>

        <div id="three_phase_power" class="calc-section">
            <h2>3 Phase Power Calculation (in kW)</h2>
            <div class="calc-card">
                <form onsubmit="calculate(event, 'three_phase_power')">
                    <div class="input-row"><label>Power =</label><input type="text" name="Power" id="Power_3p"></div>
                    <div class="input-row"><label>Current =</label><input type="text" name="Current" id="Current_3p"></div>
                    <div class="input-row"><label>Voltage =</label><input type="text" name="Voltage" id="Voltage_3p"></div>
                    <div class="input-row"><label>Power Factor =</label><input type="text" name="Power_Factor" id="PF_3p"></div>
                    <div class="input-row"><label>No. of conductors =</label><input type="text" name="No_of_conductors" id="Conductors_3p"></div>
                    <button type="submit">Calculate</button>
                    <div class="result-box" id="result-three_phase_power"></div>
                </form>
            </div>
        </div>

        <div id="delta_connection" class="calc-section">
            <h2>Delta Connection – Line & Phase Relations</h2>
            <div class="calc-card">
                <form onsubmit="calculate(event, 'delta_connection')">
                    <div class="input-row"><label>Phase Current (L-N) =</label><input type="text" name="Phase_Current_LN"></div>
                    <div class="input-row"><label>Line Current (L-L) =</label><input type="text" name="Line_Current_LL"></div>
                    <div class="input-row"><label>Phase Voltage (L-N) =</label><input type="text" name="Phase_Voltage_LN"></div>
                    <div class="input-row"><label>Line Voltage (L-L) =</label><input type="text" name="Line_Voltage_LL"></div>
                    <button type="submit">Calculate</button>
                    <div class="result-box" id="result-delta_connection"></div>
                </form>
            </div>
        </div>

        <div id="star_connection" class="calc-section">
            <h2>Star Connection – Line & Phase Relations</h2>
            <div class="calc-card">
                <form onsubmit="calculate(event, 'star_connection')">
                    <div class="input-row"><label>Phase Current (L-N) =</label><input type="text" name="Phase_Current_LN"></div>
                    <div class="input-row"><label>Line Current (L-L) =</label><input type="text" name="Line_Current_LL"></div>
                    <div class="input-row"><label>Phase Voltage (L-N) =</label><input type="text" name="Phase_Voltage_LN"></div>
                    <div class="input-row"><label>Line Voltage (L-L) =</label><input type="text" name="Line_Voltage_LL"></div>
                    <button type="submit">Calculate</button>
                    <div class="result-box" id="result-star_connection"></div>
                </form>
            </div>
        </div>
        
        <div id="power_factor" class="calc-section">
            <h2>Power Factor Calculation</h2>
            <div class="calc-card">
                <form onsubmit="calculate(event, 'power_factor')">
                    <div class="input-row"><label>Power Factor Cos(ϕ) =</label><input type="text" name="Power_Factor_Cos"></div>
                    <div class="input-row"><label>Active Power (kW) =</label><input type="text" name="Active_Power"></div>
                    <div class="input-row"><label>Apparent Power (kVA) =</label><input type="text" name="Apparent_Power"></div>
                    <button type="submit">Calculate</button>
                    <div class="result-box" id="result-power_factor"></div>
                </form>
            </div>
        </div>
        
        <div id="reactive_power" class="calc-section">
            <h2>Reactive Power Calculation</h2>
            <div class="calc-card">
                <form onsubmit="calculate(event, 'reactive_power')">
                    <div class="input-row"><label>Reactive Factor Sin(ϕ) =</label><input type="text" name="Reactive_Factor_Sin"></div>
                    <div class="input-row"><label>Reactive Power (kVAR) =</label><input type="text" name="Reactive_Power_kVAR"></div>
                    <div class="input-row"><label>Apparent Power (kVA) =</label><input type="text" name="Apparent_Power_kVA"></div>
                    <button type="submit">Calculate</button>
                    <div class="result-box" id="result-reactive_power"></div>
                </form>
            </div>
        </div>
        
        <div id="kva_to_kw" class="calc-section">
            <h2>KVA to kW Conversion</h2>
            <div class="calc-card">
                <form onsubmit="calculate(event, 'kva_to_kw')">
                    <div class="input-row"><label>Active Power (kW) =</label><input type="text" name="Active_Power_kW"></div>
                    <div class="input-row"><label>Power Factor =</label><input type="text" name="Power_Factor_Conv"></div>
                    <div class="input-row"><label>Apparent Power (kVA) =</label><input type="text" name="Apparent_Power_Conv"></div>
                    <button type="submit">Calculate</button>
                    <div class="result-box" id="result-kva_to_kw"></div>
                </form>
            </div>
        </div>
        
        <div id="three_to_single_phase" class="calc-section">
            <h2>Three Phase to Single Phase Conversion</h2>
            <div class="calc-card">
                <form onsubmit="calculate(event, 'three_to_single_phase')">
                    <div class="input-row"><label>Three phase voltage =</label><input type="text" name="Three_phase_voltage"></div>
                    <div class="input-row"><label>Multiple factor √3 =</label><input type="text" name="Multiple_factor_root3"></div>
                    <div class="input-row"><label>Single phase voltage =</label><input type="text" name="Single_phase_voltage"></div>
                    <button type="submit">Calculate</button>
                    <div class="result-box" id="result-three_to_single_phase"></div>
                </form>
            </div>
        </div>
        
    </div>

    <script>
        function showCalculator(id) {
            document.querySelectorAll('.calc-section').forEach(section => {
                section.classList.remove('active');
            });
            document.getElementById(id).classList.add('active');
        }

        async function calculate(event, calc_type) {
            event.preventDefault();
            const form = event.target;
            const formData = new FormData(form);
            const data = {
                type: calc_type,
                inputs: {}
            };
            for (let [name, value] of formData.entries()) {
                data.inputs[name] = value;
            }
            const resultDiv = document.getElementById(`result-${calc_type}`);
            resultDiv.classList.remove('success', 'error');
            resultDiv.innerHTML = 'Calculating...';
            try {
                const response = await fetch('/api/calculate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                const result = await response.json();
                if (response.ok) {
                    resultDiv.classList.add('success');
                    resultDiv.innerHTML = result.message;
                } else {
                    resultDiv.classList.add('error');
                    resultDiv.innerHTML = result.message;
                }
            } catch (e) {
                resultDiv.classList.add('error');
                resultDiv.innerHTML = 'An unexpected error occurred.';
            }
        }

        // Show the first calculator by default
        document.addEventListener('DOMContentLoaded', () => {
            showCalculator('common_formula');
        });
    </script>
</body>
</html>
"""

CALCULATIONS = {
    'common_formula': lambda Resistance, Current, Voltage: 
        f"Calculated Resistance: {Voltage / Current:.2f} Ω" if Resistance is None and Current is not None and Voltage is not None and Current != 0 else
        f"Calculated Current: {Voltage / Resistance:.2f} A" if Current is None and Voltage is not None and Resistance is not None and Resistance != 0 else
        f"Calculated Voltage: {Current * Resistance:.2f} V" if Voltage is None and Current is not None and Resistance is not None else
        "Please provide exactly two of the three values.",
    'three_phase_power': lambda Power, Current, Voltage, Power_Factor, No_of_conductors: 
        f"Calculated Power: {(math.sqrt(3) * Voltage * Current * Power_Factor) / 1000:.2f} kW" if Power is None and all(x is not None for x in [Voltage, Current, Power_Factor]) else
        f"Calculated Current: {(Power * 1000) / (math.sqrt(3) * Voltage * Power_Factor):.2f} A" if Current is None and all(x is not None for x in [Power, Voltage, Power_Factor]) and Voltage != 0 and Power_Factor != 0 else
        f"Calculated Voltage: {(Power * 1000) / (math.sqrt(3) * Current * Power_Factor):.2f} V" if Voltage is None and all(x is not None for x in [Power, Current, Power_Factor]) and Current != 0 and Power_Factor != 0 else
        f"Calculated Power Factor: {(Power * 1000) / (math.sqrt(3) * Voltage * Current):.2f}" if Power_Factor is None and all(x is not None for x in [Power, Voltage, Current]) and Voltage != 0 and Current != 0 else
        "Please provide exactly three of the four core values (Power, Current, Voltage, Power Factor).",
    'delta_connection': lambda Phase_Current_LN, Line_Current_LL, Phase_Voltage_LN, Line_Voltage_LL:
        f"Delta Connection: Line Current = {Phase_Current_LN * math.sqrt(3):.2f} A" if Phase_Current_LN is not None and Line_Current_LL is None else
        f"Delta Connection: Phase Current = {Line_Current_LL / math.sqrt(3):.2f} A" if Line_Current_LL is not None and Phase_Current_LN is None else
        f"Delta Connection: Line Voltage = {Phase_Voltage_LN:.2f} V" if Phase_Voltage_LN is not None and Line_Voltage_LL is None else
        f"Delta Connection: Phase Voltage = {Line_Voltage_LL:.2f} V" if Line_Voltage_LL is not None and Phase_Voltage_LN is None else
        "Please provide one value to calculate its relation.",
    'star_connection': lambda Phase_Current_LN, Line_Current_LL, Phase_Voltage_LN, Line_Voltage_LL:
        f"Star Connection: Line Current = {Phase_Current_LN:.2f} A" if Phase_Current_LN is not None and Line_Current_LL is None else
        f"Star Connection: Phase Current = {Line_Current_LL:.2f} A" if Line_Current_LL is not None and Phase_Current_LN is None else
        f"Star Connection: Line Voltage = {Phase_Voltage_LN * math.sqrt(3):.2f} V" if Phase_Voltage_LN is not None and Line_Voltage_LL is None else
        f"Star Connection: Phase Voltage = {Line_Voltage_LL / math.sqrt(3):.2f} V" if Line_Voltage_LL is not None and Phase_Voltage_LN is None else
        "Please provide one value to calculate its relation.",
    'power_factor': lambda Power_Factor_Cos, Active_Power, Apparent_Power:
        f"Calculated Power Factor: {Active_Power / Apparent_Power:.2f}" if Power_Factor_Cos is None and Active_Power is not None and Apparent_Power is not None and Apparent_Power != 0 else
        f"Calculated Active Power (kW): {Apparent_Power * Power_Factor_Cos:.2f}" if Active_Power is None and Apparent_Power is not None and Power_Factor_Cos is not None else
        f"Calculated Apparent Power (kVA): {Active_Power / Power_Factor_Cos:.2f}" if Apparent_Power is None and Active_Power is not None and Power_Factor_Cos is not None and Power_Factor_Cos != 0 else
        "Please provide two values.",
    'reactive_power': lambda Reactive_Factor_Sin, Reactive_Power_kVAR, Apparent_Power_kVA:
        f"Calculated Reactive Factor: {Reactive_Power_kVAR / Apparent_Power_kVA:.2f}" if Reactive_Factor_Sin is None and Reactive_Power_kVAR is not None and Apparent_Power_kVA is not None and Apparent_Power_kVA != 0 else
        f"Calculated Reactive Power (kVAR): {Apparent_Power_kVA * Reactive_Factor_Sin:.2f}" if Reactive_Power_kVAR is None and Apparent_Power_kVA is not None and Reactive_Factor_Sin is not None else
        f"Calculated Apparent Power (kVA): {Reactive_Power_kVAR / Reactive_Factor_Sin:.2f}" if Apparent_Power_kVA is None and Reactive_Power_kVAR is not None and Reactive_Factor_Sin is not None and Reactive_Factor_Sin != 0 else
        "Please provide two values.",
    'kva_to_kw': lambda Active_Power_kW, Power_Factor_Conv, Apparent_Power_Conv:
        f"Calculated Active Power (kW): {Apparent_Power_Conv * Power_Factor_Conv:.2f}" if Active_Power_kW is None and Apparent_Power_Conv is not None and Power_Factor_Conv is not None else
        f"Calculated Apparent Power (kVA): {Active_Power_kW / Power_Factor_Conv:.2f}" if Apparent_Power_Conv is None and Active_Power_kW is not None and Power_Factor_Conv is not None and Power_Factor_Conv != 0 else
        f"Calculated Power Factor: {Active_Power_kW / Apparent_Power_Conv:.2f}" if Power_Factor_Conv is None and Active_Power_kW is not None and Apparent_Power_Conv is not None and Apparent_Power_Conv != 0 else
        "Please provide exactly two of the three values.",
    'three_to_single_phase': lambda Three_phase_voltage, Multiple_factor_root3, Single_phase_voltage:
        f"Calculated Single Phase Voltage: {Three_phase_voltage / Multiple_factor_root3:.2f} V" if Single_phase_voltage is None and Three_phase_voltage is not None and Multiple_factor_root3 is not None else
        f"Calculated Three Phase Voltage: {Single_phase_voltage * Multiple_factor_root3:.2f} V" if Three_phase_voltage is None and Single_phase_voltage is not None and Multiple_factor_root3 is not None else
        "Please provide two of the three values.",
}

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/calculate', methods=['POST'])
def api_calculate():
    try:
        data = request.json
        calc_type = data.get('type')
        inputs = data.get('inputs', {})
        parsed_inputs = {key: float(value) if value and value.strip() else None for key, value in inputs.items()}
        calculation_function = CALCULATIONS.get(calc_type)
        if not calculation_function:
            return jsonify({'status': 'error', 'message': 'Invalid calculation type.'}), 400
        result = calculation_function(**parsed_inputs)
        if result:
            return jsonify({'status': 'success', 'message': result}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Invalid input. Please provide the required values.'}), 400
    except (ValueError, TypeError, ZeroDivisionError) as e:
        return jsonify({'status': 'error', 'message': f'An error occurred: {e}. Please enter valid numbers.'}), 400

if __name__ == '__main__':
    app.run(debug=True)