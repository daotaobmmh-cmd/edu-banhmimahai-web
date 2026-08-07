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
                    var certPrintArea = document.getElementById('certificate-print-area');
                    var dlBtn = Array.from(document.querySelectorAll('button')).find(el => el.textContent.includes('Tải chứng nhận'));
                    var viewBtn = Array.from(document.querySelectorAll('button')).find(el => el.textContent.includes('Xem lớn'));
                    
                    if (!certWrapper) return { status: false, msg: "Certificate scale wrapper not found (#certificate-scale-wrapper)" };
                    if (!certPrintArea) return { status: false, msg: "Certificate print area not found (#certificate-print-area)" };
                    if (!dlBtn) return { status: false, msg: "Download button not found" };
                    if (viewBtn) return { status: false, msg: "View large button found but it should be completely removed" };
                    
                    var tag = certPrintArea.tagName.toUpperCase();
                    if (tag === 'IMG' || tag === 'CANVAS') {
                        return { status: false, msg: "Certificate print area should not be an <img> or <canvas> element" };
                    }
                    
                    var rect = certWrapper.getBoundingClientRect();
                    var ratio = rect.width / rect.height;
                    var targetRatio = 1131 / 800;
                    var ratioError = Math.abs(ratio - targetRatio) / targetRatio;
                    if (ratioError > 0.01) {
                        return { status: false, msg: "Cert Aspect Ratio error: " + (ratioError * 100).toFixed(2) + "% is > 1% (Ratio: " + ratio.toFixed(4) + ")" };
                    }
                    
                    var titleEl = certPrintArea.querySelector('h3');
                    var nameEl = certPrintArea.querySelector('h2');
                    var descEl = certPrintArea.querySelector('p.max-w-4xl') || certPrintArea.querySelector('p:nth-of-type(2)');
                    var metaEl = certPrintArea.querySelector('div.text-left');
                    
                    if (!titleEl) return { status: false, msg: "Title (h3) inside certificate not found" };
                    if (!nameEl) return { status: false, msg: "Name (h2) inside certificate not found" };
                    if (!descEl) return { status: false, msg: "Description (p) inside certificate not found" };
                    if (!metaEl) return { status: false, msg: "Meta block (div.text-left) inside certificate not found" };
                    
                    var titleFs = parseInt(window.getComputedStyle(titleEl).fontSize);
                    var nameFs = parseInt(window.getComputedStyle(nameEl).fontSize);
                    var descFs = parseInt(window.getComputedStyle(descEl).fontSize);
                    var metaFs = parseInt(window.getComputedStyle(metaEl).fontSize);
                    
                    if (titleFs < 44) return { status: false, msg: "Title font-size (" + titleFs + "px) is less than 44px" };
                    if (nameFs < 64) return { status: false, msg: "Name font-size (" + nameFs + "px) is less than 64px" };
                    if (descFs < 24) return { status: false, msg: "Description font-size (" + descFs + "px) is less than 24px" };
                    if (metaFs < 22) return { status: false, msg: "Meta font-size (" + metaFs + "px) is less than 22px" };
                    
                    function getLuminance(rgbStr) {
                        var parts = rgbStr.match(/\\d+/g).map(Number);
                        var r = parts[0] / 255;
                        var g = parts[1] / 255;
                        var b = parts[2] / 255;
                        var a = [r, g, b].map(function(v) {
                            return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
                        });
                        return 0.2126 * a[0] + 0.7152 * a[1] + 0.0722 * a[2];
                    }
                    var fgColor = window.getComputedStyle(metaEl).color;
                    var bgColor = "rgb(255, 255, 255)";
                    var l1 = getLuminance(fgColor);
                    var l2 = getLuminance(bgColor);
                    var brightest = Math.max(l1, l2);
                    var darkest = Math.min(l1, l2);
                    var contrast = (brightest + 0.05) / (darkest + 0.05);
                    
                    if (contrast < 4.5) {
                        return { status: false, msg: "Meta text color contrast ratio (" + contrast.toFixed(2) + ":1) is less than 4.5:1 (fg: " + fgColor + ")" };
                    }
                    
                    var dlRect = dlBtn.getBoundingClientRect();
                    if (dlRect.height < 44) {
                        return { status: false, msg: "Download button touch height (" + dlRect.height + "px) is less than 44px" };
                    }
                    
                    return {
                        status: true,
                        ratio: ratio,
                        ratioError: ratioError,
                        dlWidth: dlRect.width,
                        dlHeight: dlRect.height,
                        msg: "Cert Aspect Ratio: " + ratio.toFixed(4) + " (Target: " + targetRatio.toFixed(4) + ", Error: " + (ratioError * 100).toFixed(2) + "%), Title FS: " + titleFs + "px (>=44), Name FS: " + nameFs + "px (>=64), Desc FS: " + descFs + "px (>=24), Meta FS: " + metaFs + "px (>=22), Contrast: " + contrast.toFixed(2) + ":1 (>=4.5:1), Download height: " + dlRect.height + "px (>=44px)"
                    };
                """)
                print(f"360px Cert Layout Assert: {cert_spec['msg']}")
                if not cert_spec['status']:
                    print("FAIL: Certificate responsive or design requirements violated!")
                    failed = True
                else:
                    print("PASS: Certificate design specifications and aspect ratio constraints match successfully!")
                    
                # Assert 5: Mock html2canvas download and verify 2x output canvas size 2262x1600
                print("Mocking html2canvas to verify high-res export logic (2262x1600)...")
                driver.execute_script("""
                    window.mockHtml2canvasCalled = false;
                    window.mockCanvasWidth = 0;
                    window.mockCanvasHeight = 0;
                    window.originalHtml2canvas = window.html2canvas;
                    
                    window.html2canvas = function(el, options) {
                        window.mockHtml2canvasCalled = true;
                        var mockScale = options && options.scale ? options.scale : 1;
                        var canvas = document.createElement('canvas');
                        canvas.width = 1131 * mockScale;
                        canvas.height = 800 * mockScale;
                        window.mockCanvasWidth = canvas.width;
                        window.mockCanvasHeight = canvas.height;
                        
                        canvas.toDataURL = function() {
                            return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=";
                        };
                        return Promise.resolve(canvas);
                    };
                    
                    var dlBtn = Array.from(document.querySelectorAll('button')).find(el => el.textContent.includes('Tải chứng nhận'));
                    if (dlBtn) {
                        dlBtn.click();
                    }
                """)
                time.sleep(2)
                
                export_spec = driver.execute_script("""
                    var passed = window.mockHtml2canvasCalled && window.mockCanvasWidth === 2262 && window.mockCanvasHeight === 1600;
                    window.html2canvas = window.originalHtml2canvas;
                    return {
                        status: passed,
                        called: window.mockHtml2canvasCalled,
                        w: window.mockCanvasWidth,
                        h: window.mockCanvasHeight,
                        msg: "html2canvas invoked: " + window.mockHtml2canvasCalled + " (Expected: true), Generated canvas size: " + window.mockCanvasWidth + "x" + window.mockCanvasHeight + "px (Expected: 2262x1600px)"
                    };
                """)
                print(f"Export high-res PNG Assert: {export_spec['msg']}")
                if not export_spec['status']:
                    print("FAIL: Certificate download function did not produce a 2262x1600 image!")
                    failed = True
                else:
                    print("PASS: High-res PNG export logic is verified and correct!")
                    
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
