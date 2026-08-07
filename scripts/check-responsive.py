import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def test_responsive():
    url = "https://daotao.banhmimahai.vn/nhuongquyen/?v=4"
    viewports = [320, 360, 390, 768, 1280]
    height = 900
    
    print(f"Starting responsive checks on URL: {url}")
    failed = False
    
    for width in viewports:
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument(f"--window-size={width},{height}")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        
        # Simulating mobile user-agent for small screens to trigger mobile routing/layout
        if width < 768:
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1")

        driver = webdriver.Chrome(options=chrome_options)
        try:
            driver.get(url)
            time.sleep(2)
            
            # Check horizontal scroll metrics
            scroll_width = driver.execute_script("return document.documentElement.scrollWidth")
            inner_width = driver.execute_script("return window.innerWidth")
            
            print(f"Viewport width {width}px: scrollWidth = {scroll_width}px, innerWidth = {inner_width}px")
            
            # Assert no horizontal overflow (allowing 1px tolerance for rounding)
            if scroll_width > inner_width + 1:
                print(f"FAIL: Horizontal overflow detected at viewport {width}px! (overflow by {scroll_width - inner_width}px)")
                
                # Identify overflowing elements
                overflowing_elements = driver.execute_script("""
                    var elements = document.querySelectorAll('*');
                    var bad = [];
                    var w = window.innerWidth;
                    for (var i = 0; i < elements.length; i++) {
                        var r = elements[i].getBoundingClientRect();
                        if (r.right > w + 1) {
                            bad.push(elements[i].tagName + '.' + elements[i].className.split(' ').join('.') + ' (right: ' + r.right + ')');
                        }
                    }
                    return bad.slice(0, 5);
                """)
                if overflowing_elements:
                    print("Top overflowing elements:")
                    for el in overflowing_elements:
                        print(f"  - {el}")
                failed = True
            else:
                print(f"PASS: No horizontal scroll at {width}px")
                
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
