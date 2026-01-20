<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IPF GL 係數計算器</title>
    <style>
        /* CSS 樣式設計 - 讓介面看起來簡潔現代 */
        :root {
            --primary-color: #0056b3;
            --bg-color: #f4f7f6;
            --card-bg: #ffffff;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            color: #333;
            display: flex;
            justify-content: center;
            padding: 20px;
            margin: 0;
        }

        .container {
            background-color: var(--card-bg);
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            width: 100%;
            max-width: 500px;
        }

        h1 {
            text-align: center;
            color: var(--primary-color);
            margin-bottom: 25px;
        }

        .form-group {
            margin-bottom: 20px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #555;
        }

        input[type="number"], select {
            width: 100%;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 8px;
            box-sizing: border-box; /* 重要：讓 padding 不會撐破寬度 */
            font-size: 16px;
            transition: border-color 0.3s;
        }

        input[type="number"]:focus, select:focus {
            border-color: var(--primary-color);
            outline: none;
        }

        .radio-group {
            display: flex;
            gap: 15px;
            margin-bottom: 15px;
        }

        .radio-label {
            display: flex;
            align-items: center;
            font-weight: normal;
            cursor: pointer;
        }

        .radio-label input {
            margin-right: 8px;
        }

        .section-title {
            font-size: 1.1em;
            color: var(--primary-color);
            margin-top: 30px;
            margin-bottom: 15px;
            border-bottom: 2px solid #eee;
            padding-bottom: 5px;
        }

        button {
            width: 100%;
            padding: 15px;
            background-color: var(--primary-color);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: background-color 0.2s;
        }

        button:hover {
            background-color: #004494;
        }

        #result-area {
            margin-top: 30px;
            padding: 20px;
            background-color: #eef6fc;
            border-radius: 10px;
            text-align: center;
            display: none; /* 預設隱藏 */
        }

        .result-label {
            font-size: 1em;
            color: #666;
        }

        .result-value {
            font-size: 2.5em;
            font-weight: bold;
            color: var(--primary-color);
            margin: 10px 0;
        }
        
        .total-weight {
            font-size: 1.2em;
            color: #333;
            margin-bottom: 5px;
        }
    </style>
</head>
<body>

<div class="container">
    <h1>🏋️‍♂️ IPF GL 計算器</h1>

    <div class="form-group">
        <label>基本設定</label>
        <div class="radio-group">
            <label class="radio-label"><input type="radio" name="gender" value="female" checked> 女生</label>
            <label class="radio-label"><input type="radio" name="gender" value="male"> 男生</label>
        </div>
        <div class="radio-group">
            <label class="radio-label"><input type="radio" name="equipment" value="raw" checked> 無裝備 (Raw)</label>
            <label class="radio-label"><input type="radio" name="equipment" value="equipped"> 有裝備 (Equipped)</label>
        </div>
        <div class="radio-group" style="margin-top:10px;">
             <label class="radio-label"><input type="radio" name="unit" value="kg" checked> 公斤 (kg)</label>
             <label class="radio-label"><input type="radio" name="unit" value="lbs"> 英磅 (lbs)</label>
        </div>
    </div>

    <div class="form-group">
        <label for="bodyweight">體重</label>
        <input type="number" id="bodyweight" placeholder="輸入體重" step="0.1">
    </div>

    <div class="section-title">三項成績</div>

    <div class="form-group">
        <label for="squat">深蹲 (Squat)</label>
        <input type="number" id="squat" placeholder="0" step="0.5">
    </div>

    <div class="form-group">
        <label for="bench">臥推 (Bench Press)</label>
        <input type="number" id="bench" placeholder="0" step="0.5">
    </div>

    <div class="form-group">
        <label for="deadlift">硬舉 (Deadlift)</label>
        <input type="number" id="deadlift" placeholder="0" step="0.5">
    </div>

    <button onclick="calculateGL()">計算 IPF GL 分數</button>

    <div id="result-area">
        <div class="total-weight">總和: <span id="totalWeightDisplay">0</span> kg</div>
        <div class="result-label">IPF GL Points</div>
        <div class="result-value" id="glScoreDisplay">0.00</div>
    </div>
</div>

<script>
    // JavaScript 計算邏輯

    // IPF GL 官方係數表 (資料來源：IPF Technical Rules Book)
    const COEFFICIENTS = {
        male: {
            raw: { A: 1199.72839, B: 1030.90069, C: 0.0092155 },
            equipped: { A: 1236.61249, B: 990.26461, C: 0.0118756 }
        },
        female: {
            raw: { A: 610.32796, B: 1045.59282, C: 0.0304889 },
            equipped: { A: 758.63878, B: 949.31382, C: 0.0243547 }
        }
    };

    function calculateGL() {
        // 1. 獲取輸入值
        const gender = document.querySelector('input[name="gender"]:checked').value;
        const equipment = document.querySelector('input[name="equipment"]:checked').value;
        const unit = document.querySelector('input[name="unit"]:checked').value;

        let bw = parseFloat(document.getElementById('bodyweight').value) || 0;
        let s = parseFloat(document.getElementById('squat').value) || 0;
        let b = parseFloat(document.getElementById('bench').value) || 0;
        let d = parseFloat(document.getElementById('deadlift').value) || 0;

        // 2. 基本驗證
        if (bw <= 0) {
            alert("請輸入有效的體重！");
            return;
        }
        if (s === 0 && b === 0 && d === 0) {
             alert("請至少輸入一項成績！");
             return;
        }

        // 3. 單位轉換 (如果選擇lbs，全部轉為kg進行計算)
        if (unit === 'lbs') {
            bw = bw * 0.45359237;
            s = s * 0.45359237;
            b = b * 0.45359237;
            d = d * 0.45359237;
        }

        // 4. 計算總和
        const total = s + b + d;

        // 5. 獲取對應的係數
        const coeff = COEFFICIENTS[gender][equipment];

        // 6. 核心公式計算 (IPF GL Formula)
        // Points = Total * 100 / ( A - B * e^(-C * Bodyweight) )
        const denominator = coeff.A - coeff.B * Math.exp(-coeff.C * bw);
        let glScore = (total * 100) / denominator;

        // 7. 顯示結果
        const resultArea = document.getElementById('result-area');
        const totalDisplay = document.getElementById('totalWeightDisplay');
        const scoreDisplay = document.getElementById('glScoreDisplay');

        resultArea.style.display = 'block'; // 顯示結果區域
        // 總和顯示小數點後1位 (例如 225.0 或 225.5)
        totalDisplay.textContent = total.toFixed(1); 
        // 分數顯示小數點後2位
        scoreDisplay.textContent = glScore.toFixed(2);

        // 滾動到結果區
        resultArea.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
</script>

</body>
</html>
