import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def test_responsive():
    url = "https://daotao.banhmimahai.vn/nhuongquyen/?v=6"
    viewports = [320, 360, 390, 768, 1280]
    height = 900
    
    print(f"Starting responsive checks on URL: {url}")
    failed = False
    
    for width in viewports:
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        
        # Configure Mobile Emulation to force exact innerWidth
        mobile_emulation = {
            "deviceMetrics": { "width": width, "height": height, "pixelRatio": 1.0, "touch": width < 768 },
            "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1" if width < 768 else "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
        }
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

        driver = webdriver.Chrome(options=chrome_options)
        try:
            driver.get(url)
            time.sleep(2)
            
            # Calibration Assert: verify window.innerWidth matches the target width
            inner_width = driver.execute_script("return window.innerWidth")
            scroll_width = driver.execute_script("return document.documentElement.scrollWidth")
            
            print(f"Viewport width TARGET: {width}px | innerWidth = {inner_width}px | scrollWidth = {scroll_width}px")
            
            if abs(inner_width - width) > 2:
                print(f"ERROR: Oracle calibration error! Expected innerWidth ~{width}px, but browser reports {inner_width}px.")
                sys.exit(2) # Exit code 2: Oracle calibration error
                
            # Assert 1: Main document scrollWidth must not overflow the TARGET width
            if scroll_width > width + 1:
                print(f"FAIL: Horizontal overflow detected! document.scrollWidth ({scroll_width}px) > target width ({width}px)")
                failed = True
            else:
                print(f"PASS: scrollWidth ({scroll_width}px) <= target width ({width}px)")
                
            # Transition to study mode & test mode to verify elements inside cards
            driver.execute_script("""
                var name_input = document.querySelector("input[placeholder='Nhập họ tên khách hàng']");
                var address_input = document.querySelector("input[placeholder='Nhập địa chỉ xe/điểm bán']");
                if (name_input && address_input) {
                    name_input.value = "Long Test";
                    name_input.dispatchEvent(new Event('input'));
                    address_input.value = "Cửa hàng Quận 1";
                    address_input.dispatchEvent(new Event('input'));
                    
                    // Click start study
                    var study_card = document.querySelector("main div.group") || document.querySelector("main .bento-card");
                    if (study_card) {
                        study_card.click();
                    }
                }
            """)
            time.sleep(2)
            
            # Assert 2: Verify element-level layouts (left >= 0, right <= innerWidth) for active panels
            overflowing_elements = driver.execute_script("""
                var elementsToCheck = [
                    document.querySelector('[x-show="currentStudyQuestion"]'),
                    document.querySelector('[x-show="currentView === \\'test\\'"] .bento-card'),
                    document.querySelector('.wrong-questions-section'),
                    document.querySelector('#certificate-print-area')
                ];
                var w = window.innerWidth;
                var bad = [];
                elementsToCheck.forEach(function(el) {
                    if (el && window.getComputedStyle(el).display !== 'none') {
                        el.scrollIntoView();
                        var rect = el.getBoundingClientRect();
                        if (rect.left < -1 || rect.right > w + 1) {
                            bad.push(el.tagName + '.' + el.className.split(' ').join('.') + ' (left: ' + rect.left + ', right: ' + rect.right + ', innerWidth: ' + w + ')');
                        }
                    }
                });
                return bad;
            """)
            
            if overflowing_elements:
                print("FAIL: The following sections have layout overflow:")
                for el in overflowing_elements:
                    print(f"  - {el}")
                failed = True
            else:
                print("PASS: Active sections are within viewport boundaries.")
                
            # Assert 3: Mobile specific layout contraction rules at 360px
            if width == 360:
                spec_passed = driver.execute_script("""
                    var card = document.querySelector('[x-show="currentStudyQuestion"]');
                    var heading = document.querySelector('#practice-question-heading');
                    var option = document.querySelector('main button span.flex-1') || document.querySelector('button span.flex-1');
                    
                    if (!card) return { status: false, msg: "Study question card not found" };
                    if (!heading) return { status: false, msg: "Question heading not found" };
                    if (!option) return { status: false, msg: "Option text not found" };
                    
                    var rect = card.getBoundingClientRect();
                    var gutter_left = rect.left;
                    
                    var heading_fs = parseInt(window.getComputedStyle(heading).fontSize);
                    var option_fs = parseInt(window.getComputedStyle(option).fontSize);
                    
                    var ok = (gutter_left <= 16) && (heading_fs >= 16) && (option_fs >= 15);
                    return {
                        status: ok,
                        gutter_left: gutter_left,
                        heading_fs: heading_fs,
                        option_fs: option_fs,
                        msg: "Gutter left: " + gutter_left + "px (<=16px), Question Font: " + heading_fs + "px (>=16px), Option Font: " + option_fs + "px (>=15px)"
                    };
                """)
                print(f"360px Layout Assert: {spec_passed['msg']}")
                if not spec_passed['status']:
                    print(f"FAIL: 360px layout contraction spec violated!")
                    failed = True
                else:
                    print(f"PASS: 360px layout spec matches responsive priority constraints!")
                
                # Assert 4: Transition to results view to verify Certificate scaling & touch targets
                print("Transitioning to Results view to verify Certificate specifications...")
                driver.execute_script("""
                    var el = document.querySelector('[x-data]');
                    var data = null;
                    if (el.__x) {
                        data = el.__x.$data;
                    } else if (el._x_dataStack) {
                        data = el._x_dataStack[0];
                    }
                    if (data) {
                        data.resultPassed = true;
                        data.currentView = 'result';
                        data.testAttemptId = 'test-12345';
                    }
                """)
                time.sleep(2)
                
                cert_spec = driver.execute_script("""
                    var certWrapper = document.getElementById('certificate-scale-wrapper');
                    var dlBtn = Array.from(document.querySelectorAll('button')).find(el => el.textContent.includes('Tải chứng nhận'));
                    
                    if (!certWrapper) return { status: false, msg: "Certificate scale wrapper not found" };
                    if (!dlBtn) return { status: false, msg: "Download button not found" };
                    
                    var rect = certWrapper.getBoundingClientRect();
                    var ratio = rect.width / rect.height;
                    var targetRatio = 1131 / 800;
                    var ratioError = Math.abs(ratio - targetRatio) / targetRatio;
                    
                    var dlRect = dlBtn.getBoundingClientRect();
                    
                    var ratioOk = ratioError <= 0.01;
                    var dlBtnOk = dlRect.width >= 44 && dlRect.height >= 44;
                    
                    var ok = ratioOk && dlBtnOk;
                    return {
                        status: ok,
                        ratio: ratio,
                        ratioError: ratioError,
                        dlWidth: dlRect.width,
                        dlHeight: dlRect.height,
                        msg: "Cert Aspect Ratio: " + ratio.toFixed(4) + " (Target: " + targetRatio.toFixed(4) + ", Error: " + (ratioError * 100).toFixed(2) + "%), Download Button Touch Target: " + dlRect.width + "x" + dlRect.height + "px (>=44px)"
                    };
                """)
                print(f"360px Cert Layout Assert: {cert_spec['msg']}")
                if not cert_spec['status']:
                    print("FAIL: Certificate responsive or touch target requirements violated!")
                    failed = True
                else:
                    print("PASS: Certificate aspect ratio scaled correctly and touch targets are valid!")
                    
        except Exception as e:
            print(f"ERROR during check at {width}px: {e}")
            failed = True
        finally:
            driver.quit()
            
    if failed:
        print("\nResult: FAIL")
        sys.exit(1)
    else:
        print("\nResult: PASS All viewports are responsive!")
        sys.exit(0)

if __name__ == "__main__":
    test_responsive()
