import cv2
import numpy as np
import pyautogui
import time
import random
import os
import json
from typing import Tuple, Dict, Optional

pyautogui.FAILSAFE = False

class NavigationBot:
    def __init__(self, config_file: str = "nav_config.json"):
        """Initialize the navigation bot"""
        self.config = self.load_config(config_file)
        self.screen_width, self.screen_height = pyautogui.size()
        
        self.cycle_count = 0
        
        self.templates = self.load_templates()
        
        print(f"Navigation Bot initialized. Screen: {self.screen_width}x{self.screen_height}")
        print(f"Loaded {len(self.templates)} templates")
    
    def load_config(self, config_file: str) -> Dict:
        """Load configuration from JSON file"""
        default_config = {
            "confidence_threshold": 0.7,
            "max_cycles": 50,
            "delay_between_cycles": 10,
            "battle_time": 120,
            "search_timeout": 30,
            "random_delay": [0.1, 0.5],
            "human_like_mouse": True,
            "auto_cancel_timeout": 45,
            "enable_auto_cancel": True
        }
        
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                user_config = json.load(f)
                default_config.update(user_config)
        
        return default_config
    
    def load_templates(self) -> Dict:
        """Load button template images"""
        templates = {}
        template_files = { 
            "attack_button": "templates/attack_button.png",
            "multiplayer_button": "templates/multiplayer_button.png",
            "find_match_button": "templates/find_match_button.png",
            "return_home": "templates/return_home.png",
            
            "cancel_attack": "templates/cancel/cancel_attack.png",
            "cancel_ok": "templates/cancel/cancel_ok.png",
        }
        
        os.makedirs("templates", exist_ok=True)
        os.makedirs("templates/cancel", exist_ok=True)
        
        for name, path in template_files.items():
            if os.path.exists(path):
                templates[name] = cv2.imread(path, 0)
        
        return templates
    
    def capture_screen(self, region: Tuple = None, grayscale: bool = False) -> np.ndarray:
        """Capture screen or region"""
        screenshot = pyautogui.screenshot(region=region)
        img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        
        if grayscale:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        return img
    
    def find_with_image(self, template_name: str, timeout: float = 5.0, 
                       confidence: float = None) -> Optional[Tuple[int, int]]:
        """
        Find image template on screen
        Returns center coordinates if found
        """
        if template_name not in self.templates:
            return None
        
        if confidence is None:
            confidence = self.config["confidence_threshold"]
        
        template = self.templates[template_name]
        h, w = template.shape
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                screen_gray = self.capture_screen(grayscale=True)
                result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, max_loc = cv2.minMaxLoc(result)
                
                if max_val >= confidence:
                    center_x = max_loc[0] + w // 2
                    center_y = max_loc[1] + h // 2
                    return (center_x, center_y)
                
                time.sleep(0.3)
                
            except Exception:
                time.sleep(1)
        
        return None
    
    def human_click(self, x: int, y: int, click_type: str = "left"):
        """Perform human-like click with natural variations"""
        if self.config["human_like_mouse"]:
            current_x, current_y = pyautogui.position()
            
            steps = random.randint(2, 4)
            for i in range(steps):
                progress = (i + 1) / steps
                segment_x = current_x + (x - current_x) * progress + random.randint(-2, 2)
                segment_y = current_y + (y - current_y) * progress + random.randint(-2, 2)
                
                pyautogui.moveTo(segment_x, segment_y, 
                               duration=random.uniform(0.05, 0.15))
                time.sleep(random.uniform(0.01, 0.03))
        
        offset_x = random.randint(-3, 3)
        offset_y = random.randint(-3, 3)
        pyautogui.moveTo(x + offset_x, y + offset_y, 
                        duration=random.uniform(0.05, 0.1))
        
        time.sleep(random.uniform(*self.config["random_delay"]))
        
        if click_type == "left":
            pyautogui.click()
        elif click_type == "right":
            pyautogui.rightClick()
        elif click_type == "double":
            pyautogui.doubleClick()
        
        time.sleep(random.uniform(0.05, 0.15))
    
    def click_button(self, button_name: str) -> bool:
        """Find and click a button using image recognition"""
        coords = self.find_with_image(button_name)
        
        if coords:
            self.human_click(coords[0], coords[1])
            return True
        
        return False
    
    def wait_for_battle_end(self, max_time: int = 180):
        """
        Wait for battle to end or timeout with auto-cancel feature
        """
        start_time = time.time()
        
        timeout = self.config.get("auto_cancel_timeout", max_time)
        
        while time.time() - start_time < timeout:
            return_coords = self.find_with_image("return_home", timeout=1)
            if return_coords:
                return True
            
            time.sleep(10)
        
        cancelled = self.cancel_attack_after_timeout(timeout)
        
        return cancelled
    
    def cancel_attack_after_timeout(self, timeout: int = 120) -> bool:
        """
        Cancel the attack after specified timeout
        Returns True if cancellation was successful
        """
        enable_auto_cancel = self.config.get("enable_auto_cancel", True)
        
        if not enable_auto_cancel:
            return False
        
        cancel_coords = self.find_with_image("cancel_attack", timeout=10)
        if cancel_coords:
            self.human_click(cancel_coords[0], cancel_coords[1])
            time.sleep(2)  
            
            ok_coords = self.find_with_image("cancel_ok", timeout=5)
            if ok_coords:
                self.human_click(ok_coords[0], ok_coords[1])
                time.sleep(3)
                return True
        
        return False
    
    def perform_attack(self):
        """
        EMPTY FUNCTION FOR FUTURE USE
        This is where attack logic would go
        Currently just waits for battle time
        """
        time.sleep(5)
    
    def navigation_cycle(self) -> bool:
        """
        Execute a single navigation cycle from home base to battle and back
        """
        try:
            if not self.click_button("attack_button"):
                print("Attack button not found!")
                return False
            
            time.sleep(random.uniform(1.5, 2.5))
            
            if not self.click_button("multiplayer_button"):
                print("Multiplayer button not found!")
                return False
            
            time.sleep(random.uniform(1.5, 2.5))
            
            if not self.click_button("find_match_button"):
                print("Find Match button not found!")
                return False
            
            time.sleep(random.uniform(8, 12))
            
            self.perform_attack()
            
            self.wait_for_battle_end(self.config["battle_time"])
            
            return_success = False
            
            if self.click_button("return_home"):
                return_success = True
            
            if not return_success:
                self.human_click(self.screen_width // 2, self.screen_height // 2)
            
            time.sleep(random.uniform(3, 5))
            
            self.cycle_count += 1
            return True
            
        except Exception:
            return False
    
    def continuous_navigation_loop(self):
        """Continuous navigation loop"""
        print(f"\nStarting continuous navigation cycles")
        print(f"Maximum cycles: {self.config['max_cycles']}")
        print(f"Delay between cycles: {self.config['delay_between_cycles']} seconds")
        print("Press Ctrl+C to stop\n")
        
        try:
            while self.cycle_count < self.config["max_cycles"]:
                print(f"\n{'='*60}")
                print(f"CYCLE #{self.cycle_count + 1}")
                print(f"{'='*60}")
                
                success = self.navigation_cycle()
                
                if success:
                    print(f"Cycle #{self.cycle_count} completed successfully")
                    
                    delay = self.config["delay_between_cycles"] + random.uniform(-5, 10)
                    
                    if self.cycle_count < self.config["max_cycles"]:
                        print(f"Next cycle in {delay:.1f} seconds...")
                        
                        for i in range(int(delay), 0, -1):
                            if i % 30 == 0 or i <= 10:
                                print(f"   {i} seconds remaining...")
                            time.sleep(1)
                        print()
                else:
                    print(f"Cycle #{self.cycle_count + 1} failed")
                    print("Waiting 30 seconds before retry...")
                    time.sleep(30)
        
        except KeyboardInterrupt:
            print("\n\nBot stopped by user")
        
        self.show_statistics()
    
    def show_statistics(self):
        """Display navigation statistics"""
        print("\n" + "="*60)
        print("NAVIGATION SESSION STATISTICS")
        print("="*60)
        print(f"Total Cycles Completed: {self.cycle_count}")
        print("="*60 + "\n")
    
    def run(self):
        """Main run function"""
        print("""
        ╔══════════════════════════════════════════════════════╗
        ║      COC NAVIGATION BOT                              ║
        ║      Menu Navigation Only                            ║
        ║      Attack function empty for future use           ║
        ║      Educational Purpose Only                       ║
        ╚══════════════════════════════════════════════════════╝
        """)
        
        required_templates = ["attack_button", "multiplayer_button", "find_match_button", "return_home"]
        cancel_templates = ["cancel_attack", "cancel_ok"]
        
        missing_templates = []
        for template in required_templates:
            if template not in self.templates:
                missing_templates.append(template)
        
        if missing_templates:
            print(f"Warning: Missing required templates: {', '.join(missing_templates)}")
            print("Place the following screenshots in 'templates/' folder:")
            print("1. attack_button.png - Attack button on main screen")
            print("2. multiplayer_button.png - Multiplayer button after attack")
            print("3. find_match_button.png - Find Match button")
            print("4. return_home.png - Return Home button after battle")
        
        missing_cancel = []
        for template in cancel_templates:
            if template not in self.templates:
                missing_cancel.append(template)
        
        if missing_cancel:
            print(f"\nWarning: Missing cancel templates: {', '.join(missing_cancel)}")
            print("Place the following screenshots in 'templates/cancel/' folder:")
            print("1. cancel_attack.png - Cancel Attack button")
            print("2. cancel_ok.png - OK button in cancel confirmation dialog")
            print("The bot requires these images for auto-cancel feature.\n")
        
        while True:
            print("\nMain Menu:")
            print("1. Single Navigation Test")
            print("2. Continuous Navigation")
            print("3. View Statistics")
            print("4. Exit")
            
            choice = input("\nSelect option (1-4): ").strip()
            
            if choice == "1":
                success = self.navigation_cycle()
                if success:
                    print("Navigation cycle completed successfully")
                else:
                    print("Navigation cycle failed")
            elif choice == "2":
                self.continuous_navigation_loop()
            elif choice == "3":
                self.show_statistics()
            elif choice == "4":
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    bot = NavigationBot()
    bot.run()