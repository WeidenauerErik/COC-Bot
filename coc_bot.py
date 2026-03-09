import cv2
import numpy as np
import random
import os
import json
import keyboard
import time
import pyautogui
from typing import Tuple, Dict, Optional

pyautogui.FAILSAFE = False

class CoCBot:
    def __init__(self, config_file: str = "bot_config.json"):
        """Initialize the bot with navigation and attack capabilities"""
        self.config = self.load_config(config_file)
        self.screen_width, self.screen_height = pyautogui.size()
        self.cycle_count = 0
        self.templates = self.load_templates()
        
        # Attack configuration
        self.attack_config = {
            "heroKeybinds": ["q", "w", "e"],
            "unitKeybind": "2",
            "zapKeybind": "a",
            "airDefensPositions": [
                [1000, 700],
                [1000, 500],
                [500, 700],
                [500, 500],
            ],
            "heroXPosition": 100,
            "heroYPosition": 500,
            "unitXPosition": 100,
            "unitYPosition": 500
        }
        
        print(f"CoC Bot initialized. Screen: {self.screen_width}x{self.screen_height}")
        print(f"Loaded {len(self.templates)} templates")

    def load_config(self, config_file: str) -> Dict:
        """Load configuration from JSON file"""
        default_config = {
            "confidence_threshold": 0.7,
            "max_cycles": 50,
            "delay_between_cycles": 10,
            "battle_time": 30,
            "search_timeout": 30,
            "random_delay": [0.1, 0.5],
            "human_like_mouse": True,
            "auto_cancel_timeout": 45,
            "enable_auto_cancel": True,
            "attack_delay_before": 2,
            "attack_delay_between": 0.3
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

    def find_with_image(self, template_name: str, timeout: float = 5.0, confidence: float = None) -> Optional[Tuple[int, int]]:
        """Find image template on screen - Returns center coordinates if found"""
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

    def find_all_air_defenses(self, timeout: float = 30.0, confidence: float = 0.75) -> list:
        """
        Find all air defense positions on the screen using template matching
        Returns a list of tuples (x, y, level) for each found air defense
        """
        print("Searching for air defenses...")
        
        # Load air defense templates if not already loaded
        air_defense_templates = {}
        template_dir = "templates/airdefense"
        
        # Check if directory exists
        if not os.path.exists(template_dir):
            print(f"Warning: Air defense template directory '{template_dir}' not found!")
            return []
        
        # Load all air defense level templates
        for level in range(8, 12):  # levels 8-11
            filename = f"airdefense_level{level}.png"
            filepath = os.path.join(template_dir, filename)
            
            if os.path.exists(filepath):
                template = cv2.imread(filepath, 0)
                if template is not None:
                    air_defense_templates[level] = template
                    print(f"Loaded template for level {level}")
                else:
                    print(f"Warning: Could not load {filename}")
            else:
                print(f"Warning: {filename} not found")
        
        if not air_defense_templates:
            print("No air defense templates found!")
            return []
        
        # Capture the screen
        start_time = time.time()
        found_positions = []  # Store (x, y, level)
        
        while time.time() - start_time < timeout and len(found_positions) < 4:
            # Capture screen in grayscale
            screen_gray = self.capture_screen(grayscale=True)
            screen_h, screen_w = screen_gray.shape
            
            # Try to find each level template
            for level, template in air_defense_templates.items():
                template_h, template_w = template.shape
                
                # Skip if template is larger than screen
                if template_h > screen_h or template_w > screen_w:
                    continue
                
                # Perform template matching
                result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
                
                # Find all matches above confidence threshold
                locations = np.where(result >= confidence)
                
                # Group nearby detections
                for pt in zip(*locations[::-1]):  # Switch to (x, y) format
                    center_x = pt[0] + template_w // 2
                    center_y = pt[1] + template_h // 2
                    
                    # Check if this position is too close to already found positions
                    is_duplicate = False
                    for found_x, found_y, found_level in found_positions:
                        distance = np.sqrt((center_x - found_x)**2 + (center_y - found_y)**2)
                        if distance < 50:  # Threshold for duplicate detection
                            is_duplicate = True
                            # Keep the higher confidence detection
                            break
                    
                    if not is_duplicate:
                        found_positions.append((center_x, center_y, level))
                        print(f"Found air defense level {level} at ({center_x}, {center_y})")
                        
                        # Optional: Draw rectangle on screen for debugging
                        if len(found_positions) == 4:
                            break
                
                if len(found_positions) >= 4:
                    break
            
            if len(found_positions) < 4:
                time.sleep(0.5)  # Wait before next scan
        
        found_positions.sort(key=lambda pos: pos[2])
        
        return found_positions

    def human_click(self, x: int, y: int, click_type: str = "left"):
        """Perform human-like click with natural variations"""
        if self.config["human_like_mouse"]:
            current_x, current_y = pyautogui.position()
            steps = random.randint(2, 4)
            
            for i in range(steps):
                progress = (i + 1) / steps
                segment_x = current_x + (x - current_x) * progress + random.randint(-2, 2)
                segment_y = current_y + (y - current_y) * progress + random.randint(-2, 2)
                pyautogui.moveTo(segment_x, segment_y, duration=random.uniform(0.05, 0.15))
                time.sleep(random.uniform(0.01, 0.03))
            
            offset_x = random.randint(-3, 3)
            offset_y = random.randint(-3, 3)
            pyautogui.moveTo(x + offset_x, y + offset_y, duration=random.uniform(0.05, 0.1))
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

    # ============ ATTACK FUNCTIONS ============
    
    def press_key(self, char: str):
        """Press a keyboard key"""
        keyboard.press(char)
        time.sleep(0.3)
        keyboard.release(char)

    def place_heroes(self, char: str):
        """Place a hero at the specified position"""
        self.press_key(char)
        pyautogui.click(x=self.attack_config["heroXPosition"], 
                       y=self.attack_config["heroYPosition"])

    def place_units(self, char: str, x_position: int, y_position: int):
        """Place units with drag motion"""
        self.press_key(char)
        pyautogui.moveTo(x_position, y_position, duration=0.07)
        time.sleep(0.2)
        pyautogui.mouseDown(button='left')
        time.sleep(0.2)
        pyautogui.moveTo(x_position + 300, y_position - 300, duration=2.5)
        time.sleep(0.2)
        pyautogui.mouseUp(button='left')

    def place_zap_on_air_defense(self, char: str, air_defense_positions: list = None):
        
        found_ads = self.find_all_air_defenses(timeout=30.0, confidence=0.6)
        if found_ads:
            positions_to_use = [(x, y) for x, y, level in found_ads]
        else:
            positions_to_use = self.attack_config["airDefensPositions"]
        
        self.press_key(char)
        time.sleep(0.5)
        
        for i, (x, y) in enumerate(positions_to_use):
            pyautogui.moveTo(x, y, duration=random.uniform(0.3, 0.6))
            time.sleep(random.uniform(0.2, 0.4))
            
            for zap_num in range(3):
                pyautogui.click(x, y)
                time.sleep(random.uniform(0.2, 0.3))
            
            if i < len(positions_to_use) - 1:
                time.sleep(random.uniform(0.5, 1.0))

    def perform_attack_sequence(self):
        """Execute the complete attack sequence"""
        print("Starting attack sequence...")
        time.sleep(self.config.get("attack_delay_before", 2))
        
        # Zap air defenses first
        print("Placing zaps on air defenses...")
        self.place_zap_on_air_defense(
            self.attack_config["zapKeybind"], 
            self.attack_config["airDefensPositions"]
        )
        
        time.sleep(self.config.get("attack_delay_between", 1))
        
        # Place heroes
        print("Deploying heroes...")
        for char in self.attack_config["heroKeybinds"]:
            self.place_heroes(char)
            time.sleep(self.config.get("attack_delay_between", 1))
        
        time.sleep(self.config.get("attack_delay_between", 1))
        
        # Place units
        print("Deploying troops...")
        self.place_units(
            self.attack_config["unitKeybind"],
            self.attack_config["unitXPosition"],
            self.attack_config["unitYPosition"]
        )
        
        print("Attack sequence completed")

    # ============ BATTLE MANAGEMENT ============

    def wait_for_battle_end(self, max_time: int = 180):
        """Wait for battle to end or timeout with auto-cancel feature"""
        start_time = time.time()
        timeout = self.config.get("auto_cancel_timeout", max_time)

        while time.time() - start_time < timeout:
            return_coords = self.find_with_image("return_home", timeout=1)
            if return_coords:
                print("Battle ended normally")
                return True
            time.sleep(10)

        print(f"Battle timeout reached ({timeout} seconds)")
        cancelled = self.cancel_attack_after_timeout(timeout)
        return cancelled

    def cancel_attack_after_timeout(self, timeout: int = 120) -> bool:
        """Cancel the attack after specified timeout"""
        enable_auto_cancel = self.config.get("enable_auto_cancel", True)
        
        if not enable_auto_cancel:
            return False

        print("Attempting to cancel attack...")
        cancel_coords = self.find_with_image("cancel_attack", timeout=10)
        if cancel_coords:
            self.human_click(cancel_coords[0], cancel_coords[1])
            time.sleep(2)
            
            ok_coords = self.find_with_image("cancel_ok", timeout=5)
            if ok_coords:
                self.human_click(ok_coords[0], ok_coords[1])
                time.sleep(3)
                print("Attack cancelled successfully")
                return True
        
        return False

    def perform_attack(self):
        """Main attack function - integrates attack sequence with battle management"""
        print("\n--- Starting Battle ---")
        
        # Execute the attack sequence
        self.perform_attack_sequence()
        
        # Wait for battle to end or cancel
        print("Waiting for battle to end...")
        self.wait_for_battle_end(self.config["battle_time"])
        
        print("--- Battle Finished ---\n")

    # ============ NAVIGATION FUNCTIONS ============

    def navigation_cycle(self) -> bool:
        """Execute a single navigation cycle from home base to battle and back"""
        try:
            # Click Attack button
            if not self.click_button("attack_button"):
                print("Attack button not found!")
                return False
            time.sleep(random.uniform(1.5, 2.5))

            # Click Multiplayer button
            if not self.click_button("multiplayer_button"):
                print("Multiplayer button not found!")
                return False
            time.sleep(random.uniform(1.5, 2.5))

            # Click Find Match button
            if not self.click_button("find_match_button"):
                print("Find Match button not found!")
                return False
            
            # Wait for match to load
            time.sleep(random.uniform(8, 12))

            # Perform the actual attack
            self.perform_attack()

            # Return home
            return_success = False
            if self.click_button("return_home"):
                return_success = True
            
            if not return_success:
                print("Return home button not found, clicking center screen...")
                self.human_click(self.screen_width // 2, self.screen_height // 2)
                time.sleep(random.uniform(3, 5))

            self.cycle_count += 1
            return True

        except Exception as e:
            print(f"Navigation cycle error: {e}")
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
                    
                    if self.cycle_count < self.config["max_cycles"]:
                        delay = self.config["delay_between_cycles"] + random.uniform(-5, 10)
                        print(f"Next cycle in {delay:.1f} seconds...")
                        
                        for i in range(int(delay), 0, -1):
                            if i % 30 == 0 or i <= 10:
                                print(f"  {i} seconds remaining...")
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
        print("BOT SESSION STATISTICS")
        print("="*60)
        print(f"Total Cycles Completed: {self.cycle_count}")
        print("="*60 + "\n")

    def update_attack_config(self):
        """Interactive menu to update attack configuration"""
        print("\n=== Attack Configuration ===")
        print(f"Current hero positions: X={self.attack_config['heroXPosition']}, Y={self.attack_config['heroYPosition']}")
        print(f"Current unit positions: X={self.attack_config['unitXPosition']}, Y={self.attack_config['unitYPosition']}")
        print(f"Hero keybinds: {self.attack_config['heroKeybinds']}")
        print(f"Unit keybind: {self.attack_config['unitKeybind']}")
        print(f"Zap keybind: {self.attack_config['zapKeybind']}")
        print(f"Air defense positions: {self.attack_config['airDefensPositions']}")
        
        print("\nOptions:")
        print("1. Update hero positions")
        print("2. Update unit positions")
        print("3. Update keybinds")
        print("4. Update air defense positions")
        print("5. Back to main menu")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == "1":
            try:
                x = int(input("Enter hero X position: "))
                y = int(input("Enter hero Y position: "))
                self.attack_config["heroXPosition"] = x
                self.attack_config["heroYPosition"] = y
                print("Hero positions updated!")
            except ValueError:
                print("Invalid input!")
        
        elif choice == "2":
            try:
                x = int(input("Enter unit X position: "))
                y = int(input("Enter unit Y position: "))
                self.attack_config["unitXPosition"] = x
                self.attack_config["unitYPosition"] = y
                print("Unit positions updated!")
            except ValueError:
                print("Invalid input!")
        
        elif choice == "3":
            print("Enter new keybinds (single characters):")
            hero1 = input("Hero 1 key (default q): ") or "q"
            hero2 = input("Hero 2 key (default w): ") or "w"
            hero3 = input("Hero 3 key (default e): ") or "e"
            unit = input("Unit key (default 1): ") or "1"
            zap = input("Zap key (default a): ") or "a"
            
            self.attack_config["heroKeybinds"] = [hero1, hero2, hero3]
            self.attack_config["unitKeybind"] = unit
            self.attack_config["zapKeybind"] = zap
            print("Keybinds updated!")
        
        elif choice == "4":
            print("Enter 4 air defense positions as X,Y coordinates:")
            positions = []
            for i in range(4):
                try:
                    coords = input(f"Position {i+1} (format: x,y): ").strip().split(',')
                    if len(coords) == 2:
                        x = int(coords[0].strip())
                        y = int(coords[1].strip())
                        positions.append([x, y])
                except:
                    print(f"Invalid input for position {i+1}, keeping original")
            
            if len(positions) == 4:
                self.attack_config["airDefensPositions"] = positions
                print("Air defense positions updated!")
            else:
                print("Failed to update positions - need exactly 4 positions")

    def run(self):
        """Main run function"""
        print("""
    +----------------------------------------------------+
    |                COC COMPLETE BOT                    |
    |         Navigation + Automated Attacks              |
    |              Educational Purpose Only               |
    +----------------------------------------------------+
        """)

        # Check for required templates
        required_templates = ["attack_button", "multiplayer_button", "find_match_button", "return_home"]
        cancel_templates = ["cancel_attack", "cancel_ok"]
        
        missing_templates = []
        for template in required_templates:
            if template not in self.templates:
                missing_templates.append(template)

        if missing_templates:
            print(f"Warning: Missing required templates: {', '.join(missing_templates)}")
            print("Place the following screenshots in 'templates/' folder:")
            for template in required_templates:
                print(f"  - {template}.png")

        missing_cancel = []
        for template in cancel_templates:
            if template not in self.templates:
                missing_cancel.append(template)

        if missing_cancel:
            print(f"\nWarning: Missing cancel templates: {', '.join(missing_cancel)}")
            print("Auto-cancel feature may not work properly.")

        while True:
            print("\n=== MAIN MENU ===")
            print("1. Single Navigation + Attack Test")
            print("2. Continuous Navigation + Attack Loop")
            print("3. Configure Attack Settings")
            print("4. View Statistics")
            print("5. Exit")
            
            choice = input("\nSelect option (1-5): ").strip()

            if choice == "1":
                print("\n--- Single Test Cycle ---")
                success = self.navigation_cycle()
                if success:
                    print("Cycle completed successfully")
                else:
                    print("Cycle failed")

            elif choice == "2":
                self.continuous_navigation_loop()

            elif choice == "3":
                self.update_attack_config()

            elif choice == "4":
                self.show_statistics()

            elif choice == "5":
                print("Exiting...")
                break

            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    bot = CoCBot()
    bot.run()