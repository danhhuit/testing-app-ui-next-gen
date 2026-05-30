# NextGen UI Testing Framework

Dự án **NextGen UI Testing Framework** là một Proof of Concept cho kiểm thử giao diện thế hệ mới. Project kết hợp nhiều nhóm công cụ kiểm thử hiện đại để bao phủ nhiều khía cạnh chất lượng phần mềm:

- **Playwright + pytest**: kiểm thử chức năng Web UI.
- **Percy**: kiểm thử visual regression bằng snapshot.
- **Appium**: kiểm thử mobile web trên Android Emulator.
- **BrowserStack**: chạy Playwright test trên cloud browser.
- **k6**: kiểm thử hiệu năng ở tầng HTTP.
- **Allure / pytest-html**: xuất báo cáo test local.
- **GitHub Actions**: CI/CD pipeline tự động.

Project sử dụng website demo: <https://www.saucedemo.com/>.

---

## 1. Mục tiêu đề tài

Mục tiêu của project là chứng minh rằng kiểm thử UI hiện đại không chỉ dừng ở việc kiểm tra chức năng đúng/sai. Một framework kiểm thử tốt cần bao phủ:

| Nhóm kiểm thử | Công cụ | Mục tiêu |
|---|---|---|
| Functional Testing | Playwright, pytest | Kiểm tra hành vi chức năng như login, cart, checkout |
| Visual Regression Testing | Percy | Phát hiện lỗi màu sắc, font, layout, ảnh, style button |
| Mobile Cross-platform Testing | Appium | Kiểm thử web/app trên môi trường Android thực tế hơn |
| Cloud Browser Testing | BrowserStack | Chạy test trên cloud browser/device, có video và log |
| Performance Testing | k6 | Đo response time, tỷ lệ lỗi request, virtual users |
| Reporting | Allure, pytest-html | Hiển thị báo cáo pass/fail và chi tiết lỗi |

---

## 2. Cấu trúc thư mục

```text
NextGen-UI-Testing/
├── tests/
│   ├── pages/
│   │   ├── login_page.py
│   │   ├── inventory_page.py
│   │   └── cart_page.py
│   ├── utils/
│   │   └── fixtures.py
│   ├── test_login_flow.py
│   ├── test_inventory_and_cart.py
│   ├── test_checkout_flow.py
│   ├── test_product_detail.py
│   ├── test_mobile_flow.py
│   ├── test_visual_bugs_demo.py
│   └── test_web_flow.py
├── tests_appium/
│   └── test_appium_mobile_web.py
├── tests_cloud/
│   └── test_browserstack_direct.py
├── performance/
│   └── saucedemo_smoke.js
├── .github/
│   └── workflows/
│       └── ui-tests.yml
├── browserstack.yml
├── conftest.py
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## 3. Công nghệ sử dụng

| Công nghệ | Vai trò |
|---|---|
| Python 3.11 | Ngôn ngữ chính để viết test |
| pytest | Test runner |
| Playwright | Web UI automation |
| Percy | Visual testing / snapshot comparison |
| Appium | Mobile automation |
| UiAutomator2 | Android automation driver cho Appium |
| BrowserStack | Cloud browser testing |
| k6 | Performance testing |
| Allure Report | Báo cáo test trực quan |
| pytest-html | Báo cáo HTML đơn giản |
| GitHub Actions | CI/CD pipeline |

---

## 4. Cài đặt môi trường local

### 4.1. Vào project và tạo môi trường ảo

```powershell
cd D:\python\NextGen-UI-Testing
python -m venv venv
.\venv\Scripts\activate
```

### 4.2. Cài Python dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4.3. Cài browser cho Playwright

```powershell
python -m playwright install chromium
```

### 4.4. Cài Percy CLI

```powershell
npm install -g @percy/cli
```

### 4.5. Cài Appium server và Android driver

```powershell
npm install -g appium
appium driver install --source=npm appium-uiautomator2-driver@4.2.9
appium driver list --installed
```

### 4.6. Cài k6

```powershell
winget install k6 --source winget
k6 version
```

Nếu PowerShell chưa nhận lệnh `k6`, chạy bằng đường dẫn đầy đủ:

```powershell
& "C:\Program Files\k6\k6.exe" version
```

### 4.7. Cài Allure CLI

```powershell
npm install -g allure-commandline
allure --version
```

---

## 5. Chạy Playwright Functional Test

### Chạy test login

```powershell
python -m pytest tests\test_login_flow.py -v
```

### Chạy toàn bộ test web local

```powershell
python -m pytest tests\ -v
```

### Chạy từng nhóm test

```powershell
python -m pytest tests\test_login_flow.py -v
python -m pytest tests\test_inventory_and_cart.py -v
python -m pytest tests\test_checkout_flow.py -v
python -m pytest tests\test_product_detail.py -v
python -m pytest tests\test_mobile_flow.py -v
python -m pytest tests\test_visual_bugs_demo.py -v
python -m pytest tests\test_web_flow.py -v
```

---

## 6. Chạy Percy Visual Testing

### Set Percy token

```powershell
$env:PERCY_TOKEN="token_cua_ban"
```

Không commit token vào GitHub.

### Chạy visual bugs demo

```powershell
npx percy exec -- python -m pytest tests\test_visual_bugs_demo.py -v
```

### Chạy toàn bộ test web với Percy

```powershell
npx percy exec -- python -m pytest tests\ -v
```

Sau khi chạy, mở Percy Dashboard để xem visual snapshot và visual diff.

---

## 7. Chạy Appium Mobile Cross-platform Test

Appium test yêu cầu 3 cửa sổ PowerShell riêng.

### Cửa sổ 1: Mở Android Emulator

```powershell
& "C:\Android\Sdk\emulator\emulator.exe" -avd Pixel_7_-_Mai_Tinh
```

Kiểm tra emulator:

```powershell
adb devices
```

Kết quả đúng:

```text
emulator-5554   device
```

### Cửa sổ 2: Mở Appium server

Nếu port 4723 đang bị chiếm:

```powershell
$pid4723 = (Get-NetTCPConnection -LocalPort 4723 -ErrorAction SilentlyContinue).OwningProcess
if ($pid4723) { Stop-Process -Id $pid4723 -Force }
```

Mở Appium:

```powershell
appium --allow-insecure chromedriver_autodownload
```

Giữ cửa sổ này mở.

### Cửa sổ 3: Chạy Appium test

```powershell
cd D:\python\NextGen-UI-Testing
.\venv\Scripts\activate
$env:ANDROID_UDID="emulator-5554"
python -m pytest tests_appium\test_appium_mobile_web.py -v
```

---

## 8. Chạy BrowserStack Cloud Testing

Project sử dụng file `tests_cloud/test_browserstack_direct.py` để kết nối trực tiếp Playwright tới BrowserStack Cloud bằng WebSocket CDP.

### Set BrowserStack credentials

```powershell
$env:BROWSERSTACK_USERNAME="username_cua_ban"
$env:BROWSERSTACK_ACCESS_KEY="access_key_cua_ban"
```

Không echo key ra màn hình, không commit key lên GitHub.

### Kiểm tra file `browserstack.yml`

```powershell
Get-Content .\browserstack.yml
```

Nội dung nên có dạng:

```yaml
userName: ${BROWSERSTACK_USERNAME}
accessKey: ${BROWSERSTACK_ACCESS_KEY}
```

### Chạy BrowserStack cloud direct test

```powershell
python -m pytest .\tests_cloud\test_browserstack_direct.py -v -s
```

Sau khi chạy, mở BrowserStack Automate Dashboard để xem video, console log và network log.

---

## 9. Chạy k6 Performance Testing

### Chạy performance script

```powershell
k6 run .\performance\saucedemo_smoke.js
```

Nếu PATH chưa nhận k6:

```powershell
& "C:\Program Files\k6\k6.exe" run .\performance\saucedemo_smoke.js
```

### Chạy nhanh để demo

```powershell
& "C:\Program Files\k6\k6.exe" run --vus 3 --duration 15s .\performance\saucedemo_smoke.js
```

Các chỉ số cần quan sát:

| Chỉ số | Ý nghĩa |
|---|---|
| checks | Tỷ lệ điều kiện kiểm tra pass |
| http_req_duration | Thời gian phản hồi request |
| http_req_failed | Tỷ lệ request lỗi |
| vus | Số virtual users |
| iterations | Số vòng lặp đã chạy |

---

## 10. Xuất báo cáo local bằng pytest-html

```powershell
mkdir reports
python -m pytest tests\ -v --html=reports\full_web_report.html --self-contained-html
Invoke-Item .\reports\full_web_report.html
```

---

## 11. Xuất báo cáo local bằng Allure

### Chạy toàn bộ web local và sinh dữ liệu Allure

```powershell
Remove-Item -Recurse -Force .\allure-results -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force .\allure-report -ErrorAction SilentlyContinue
python -m pytest tests\ -v --alluredir=allure-results
```

### Mở Allure report

```powershell
allure serve allure-results
```

### Tạo report tĩnh

```powershell
allure generate allure-results --clean -o allure-report
allure open allure-report
```

Lưu ý: không nên gộp toàn bộ `tests`, `tests_appium`, `tests_cloud` trong một lệnh duy nhất khi demo, vì các nhóm test chạy trên môi trường khác nhau.

---

## 12. Lệnh demo nhanh khuyến nghị

### Web local + Allure

```powershell
cd D:\python\NextGen-UI-Testing
.\venv\Scripts\activate
Remove-Item -Recurse -Force .\allure-results -ErrorAction SilentlyContinue
python -m pytest tests\ -v --alluredir=allure-results
allure serve allure-results
```

### Appium riêng

```powershell
$env:ANDROID_UDID="emulator-5554"
python -m pytest tests_appium\test_appium_mobile_web.py -v
```

### BrowserStack riêng

```powershell
$env:BROWSERSTACK_USERNAME="username_cua_ban"
$env:BROWSERSTACK_ACCESS_KEY="access_key_cua_ban"
python -m pytest .\tests_cloud\test_browserstack_direct.py -v -s
```

### k6 riêng

```powershell
& "C:\Program Files\k6\k6.exe" run .\performance\saucedemo_smoke.js
```

---

## 13. CI/CD với GitHub Actions

CI/CD được đặt tại:

```text
.github/workflows/ui-tests.yml
```

Workflow gồm các nhóm job chính:

- Web UI tests bằng Playwright/pytest.
- Optional Appium mobile tests.
- Optional BrowserStack cloud tests.
- k6 performance smoke test.
- Upload test reports/artifacts.

Các secret nên cấu hình trong GitHub Repository Settings:

| Secret | Dùng cho |
|---|---|
| PERCY_TOKEN | Percy Visual Testing |
| BROWSERSTACK_USERNAME | BrowserStack Cloud Testing |
| BROWSERSTACK_ACCESS_KEY | BrowserStack Cloud Testing |

---

## 14. Git commands

```powershell
git status
git add .
git commit -m "Danh: update README requirements and CI/CD"
git push
```

---

## 15. Demo script nói ngắn gọn

Project này là framework kiểm thử giao diện thế hệ mới. Playwright dùng để kiểm thử chức năng web, Percy kiểm thử visual regression, Appium kiểm thử mobile web trên Android Emulator, BrowserStack chạy test trên cloud browser, k6 đo hiệu năng HTTP, còn Allure và pytest-html dùng để hiển thị báo cáo local. Nhờ đó project bao phủ nhiều góc nhìn của kiểm thử hiện đại: functional, visual, mobile, cloud, performance và reporting.
