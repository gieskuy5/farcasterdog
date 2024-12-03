import requests
import json
import time
import os
from typing import Dict, Optional, List
from datetime import datetime, timedelta

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'

class FarDog:
    def __init__(self):
        self.base_url = "https://api.fardog.xyz"
        self.token_file = "token.txt"
        self.headers = {
            "Accept": "application/json",
            "Origin": "https://fardog.xyz",
            "Referer": "https://fardog.xyz/",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
        }

    def load_tokens(self) -> List[str]:
        """Load all tokens from token.txt file"""
        tokens = []
        if os.path.exists(self.token_file):
            with open(self.token_file, "r") as f:
                tokens = [line.strip() for line in f if line.strip()]
        return tokens

    def get_user_data(self, jwt_token: str) -> Optional[Dict]:
        verify_url = f"{self.base_url}/api/user/select"
        headers = {**self.headers, "Cookie": f"token={jwt_token}"}
        try:
            response = requests.get(verify_url, headers=headers)
            if response.status_code == 200:
                return response.json()[0]
            return None
        except Exception as e:
            print(f"{Colors.RED}[-] Error getting user data: {str(e)}{Colors.RESET}")
            return None

    def get_updated_points(self, fid: int, jwt_token: str) -> Optional[int]:
        url = f"{self.base_url}/api/point/select_point_by_fid"
        headers = {**self.headers, "Cookie": f"token={jwt_token}"}
        payload = {"fid": fid}
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                data = response.json()
                return data[0]['Point']
            return None
        except Exception as e:
            print(f"{Colors.RED}[-] Error getting updated points: {str(e)}{Colors.RESET}")
            return None

    def update_points(self, task_id: int, fid: int, points: int, jwt_token: str) -> bool:
        url = f"{self.base_url}/api/user/update_point"
        headers = {**self.headers, "Cookie": f"token={jwt_token}"}
        payload = {
            "taskId": task_id,
            "fid": fid,
            "point": points
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                result = response.json()
                return result.get("code") == "1712" and "Point update successful" in result.get("message", "")
            return False
        except Exception as e:
            print(f"{Colors.RED}[-] Error updating points: {str(e)}{Colors.RESET}")
            return False

    def display_user_info(self, user_data: Dict) -> None:
        print(f"\n{Colors.GREEN}[+] Login Success !!!{Colors.RESET}")
        print(f"{Colors.BLUE}[+] userName : {Colors.YELLOW}{user_data['userName']}{Colors.RESET}")
        print(f"{Colors.BLUE}[+] fid      : {Colors.YELLOW}{user_data['fid']}{Colors.RESET}")
        print(f"{Colors.BLUE}[+] Point    : {Colors.YELLOW}{user_data['Point']}{Colors.RESET}")
        print(f"{Colors.BLUE}[+] Follow   : {Colors.YELLOW}{user_data['followCount']}{Colors.RESET}")
        print(f"{Colors.BLUE}[+] Time     : {Colors.YELLOW}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.RESET}")

    def get_daily_tasks(self, fid_id: int, jwt_token: str) -> List[Dict]:
        url = f"{self.base_url}/api/user/all_task/task_daily"
        headers = {**self.headers, "Cookie": f"token={jwt_token}"}
        payload = {
            "fidId": fid_id,
            "page": 1,
            "limit": 10
        }
        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print(f"{Colors.RED}[-] Error getting daily tasks: {str(e)}{Colors.RESET}")
            return []

    def get_main_tasks(self, fid_id: int, jwt_token: str) -> List[Dict]:
        url = f"{self.base_url}/api/user/all_task/task_main"
        headers = {**self.headers, "Cookie": f"token={jwt_token}"}
        payload = {"fidId": fid_id}
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print(f"{Colors.RED}[-] Error getting main tasks: {str(e)}{Colors.RESET}")
            return []

    def click_task(self, task_id: int, fid: int, task_name: str, jwt_token: str) -> bool:
        url = f"{self.base_url}/api/user/reg_click_status"
        headers = {**self.headers, "Cookie": f"token={jwt_token}"}
        payload = {
            "taskId": task_id,
            "fid": fid,
            "taskName": task_name,
            "clickStatus": None
        }
        try:
            response = requests.post(url, headers=headers, json=payload)
            result = response.json()
            return response.status_code == 200 and "Insert or update successful" in result.get("message", "")
        except Exception as e:
            print(f"{Colors.RED}[-] Error clicking task: {str(e)}{Colors.RESET}")
            return False

    def update_task_status(self, fid_id: int, task_id: int, jwt_token: str) -> Dict:
        url = f"{self.base_url}/api/user/task/task_daily/select_updated_task"
        headers = {**self.headers, "Cookie": f"token={jwt_token}"}
        payload = {
            "fidId": fid_id,
            "taskId": task_id
        }
        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                return response.json()[0]
            return {}
        except Exception as e:
            print(f"{Colors.RED}[-] Error updating task status: {str(e)}{Colors.RESET}")
            return {}

    def open_magic_chest(self, jwt_token: str) -> Optional[int]:
        """
        Opens the magic chest and returns the bonus points received
        """
        url = f"{self.base_url}/api/farcaster_dog/open_magic_chest"
        headers = {**self.headers, "Cookie": f"token={jwt_token}"}
        
        try:
            response = requests.post(url, headers=headers)
            if response.status_code == 200:
                result = response.json()
                return result.get('bonus')
            return None
        except Exception as e:
            print(f"{Colors.RED}[-] Error opening magic chest: {str(e)}{Colors.RESET}")
            return None

    def process_tasks(self, user_data: Dict, jwt_token: str):
        fid_id = user_data['fid']
        print(f"\n{Colors.BLUE}[+] Starting Daily Tasks Processing...{Colors.RESET}")
        
        # Try to open magic chest first
        print(f"\n{Colors.BLUE}[+] Attempting to open magic chest...{Colors.RESET}")
        bonus = self.open_magic_chest(jwt_token)
        if bonus:
            print(f"{Colors.GREEN}[+] Successfully opened magic chest! Received {bonus} bonus points{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}[*] No magic chest available or already opened{Colors.RESET}")
        
        tasks = self.get_daily_tasks(fid_id, jwt_token)
        if not tasks:
            print(f"{Colors.RED}[-] No daily tasks found{Colors.RESET}")
            return

        print(f"{Colors.CYAN}[+] Found {len(tasks)} daily tasks to process{Colors.RESET}")
        
        total_points_gained = 0
        for task in tasks:
            task_id = task['taskId']
            task_name = task['taskName']
            task_points = task['point']
            social_type = task['socialType']
            task_link = task['link']
            
            print(f"\n{Colors.BLUE}[+] Processing Task:{Colors.RESET}")
            print(f"{Colors.YELLOW}    Name: {task_name}")
            print(f"    Points: {task_points}")
            print(f"    Type: {'Telegram' if social_type == 2 else 'Twitter' if social_type == 1 else 'Other'}")
            print(f"    Link: {task_link}{Colors.RESET}")
            
            # Click task
            print(f"{Colors.BLUE}    -> Clicking task...{Colors.RESET}")
            if self.click_task(task_id, fid_id, task_name, jwt_token):
                print(f"{Colors.GREEN}    -> Task clicked successfully{Colors.RESET}")
                time.sleep(2)  # Wait after clicking
                
                # Update task status
                print(f"{Colors.BLUE}    -> Checking task status...{Colors.RESET}")
                updated_task = self.update_task_status(fid_id, task_id, jwt_token)
                if updated_task.get('clickStatus') == 1:
                    # Claim points
                    print(f"{Colors.BLUE}    -> Claiming points...{Colors.RESET}")
                    if self.update_points(task_id, fid_id, task_points, jwt_token):
                        total_points_gained += task_points
                        print(f"{Colors.GREEN}    -> Successfully claimed {task_points} points{Colors.RESET}")
                    else:
                        print(f"{Colors.RED}    -> Failed to claim points{Colors.RESET}")
                else:
                    print(f"{Colors.RED}    -> Task not ready to claim (status: {updated_task.get('clickStatus')}){Colors.RESET}")
                
                time.sleep(2)  # Wait before next task
            else:
                print(f"{Colors.RED}    -> Failed to process task{Colors.RESET}")

        # Get updated points
        print(f"\n{Colors.BLUE}[+] Checking final results...{Colors.RESET}")
        new_points = self.get_updated_points(fid_id, jwt_token)
        if new_points is not None:
            print(f"{Colors.GREEN}[+] Total points gained: {total_points_gained}")
            print(f"[+] Current total points: {new_points}{Colors.RESET}")
        else:
            print(f"{Colors.RED}[-] Failed to get updated point balance{Colors.RESET}")

        print(f"\n{Colors.GREEN}=== [ Daily tasks processing completed! ] ==={Colors.RESET}\n")

    def process_main_tasks(self, user_data: Dict, jwt_token: str):
        fid_id = user_data['fid']
        print(f"\n{Colors.BLUE}[+] Starting Main Tasks Processing...{Colors.RESET}")
        
        tasks = self.get_main_tasks(fid_id, jwt_token)
        if not tasks:
            print(f"{Colors.RED}[-] No main tasks found{Colors.RESET}")
            return

        # Filter out tasks that are already claimed
        unclaimed_tasks = [task for task in tasks if task.get('claimStatus') != 1]
        
        if not unclaimed_tasks:
            print(f"{Colors.YELLOW}[+] All main tasks have been completed!{Colors.RESET}")
            return

        print(f"{Colors.CYAN}[+] Found {len(unclaimed_tasks)} unclaimed main tasks to process{Colors.RESET}")
        
        total_points_gained = 0
        for task in unclaimed_tasks:
            task_id = task['taskId']
            task_name = task['taskName']
            task_points = task['point']
            social_type = task['socialType']
            task_link = task['link']
            
            print(f"\n{Colors.BLUE}[+] Processing Main Task:{Colors.RESET}")
            print(f"{Colors.YELLOW}    Name: {task_name}")
            print(f"    Points: {task_points}")
            print(f"    Type: {'Telegram' if social_type == 2 else 'Twitter' if social_type == 1 else 'Other'}")
            print(f"    Link: {task_link}{Colors.RESET}")
            
            # Click task
            print(f"{Colors.BLUE}    -> Clicking task...{Colors.RESET}")
            if self.click_task(task_id, fid_id, task_name, jwt_token):
                print(f"{Colors.GREEN}    -> Task clicked successfully{Colors.RESET}")
                time.sleep(2)  # Wait after clicking
                
                # Get updated task status
                updated_tasks = self.get_main_tasks(fid_id, jwt_token)
                updated_task = next((t for t in updated_tasks if t['taskId'] == task_id), None)
                
                if updated_task and updated_task.get('clickStatus') == 1:
                    # Claim points
                    print(f"{Colors.BLUE}    -> Claiming points...{Colors.RESET}")
                    if self.update_points(task_id, fid_id, task_points, jwt_token):
                        total_points_gained += task_points
                        print(f"{Colors.GREEN}    -> Successfully claimed {task_points} points{Colors.RESET}")
                    else:
                        print(f"{Colors.RED}    -> Failed to claim points{Colors.RESET}")
                else:
                    print(f"{Colors.RED}    -> Task not ready to claim{Colors.RESET}")
                
                time.sleep(2)  # Wait before next task
            else:
                print(f"{Colors.RED}    -> Failed to process task{Colors.RESET}")

        if total_points_gained > 0:
            # Get updated points
            print(f"\n{Colors.BLUE}[+] Checking final results...{Colors.RESET}")
            new_points = self.get_updated_points(fid_id, jwt_token)
            if new_points is not None:
                print(f"{Colors.GREEN}[+] Total points gained: {total_points_gained}")
                print(f"[+] Current total points: {new_points}{Colors.RESET}")
            else:
                print(f"{Colors.RED}[-] Failed to get updated point balance{Colors.RESET}")

        print(f"\n{Colors.GREEN}=== [ Main tasks processing completed! ] ==={Colors.RESET}\n")

    def start(self) -> None:
        while True:  # Add infinite loop to keep the bot running
            start_time = datetime.now()
            print(f"\n{Colors.CYAN}=== Starting New Cycle at {start_time.strftime('%Y-%m-%d %H:%M:%S')} ==={Colors.RESET}")
            print(f"{Colors.CYAN}[+] Starting FarDog Bot (Multi-Account Mode)...{Colors.RESET}")
            
            tokens = self.load_tokens()
            if not tokens:
                print(f"{Colors.RED}[-] No tokens found in token.txt. Please add your tokens first.{Colors.RESET}")
                return

            print(f"{Colors.CYAN}[+] Found {len(tokens)} accounts to process{Colors.RESET}")
            
            for index, jwt_token in enumerate(tokens, 1):
                print(f"\n{Colors.CYAN}=== Processing Account {index}/{len(tokens)} ==={Colors.RESET}")
                
                print(f"{Colors.BLUE}[+] Loading user data...{Colors.RESET}")
                user_data = self.get_user_data(jwt_token)
                if not user_data:
                    print(f"{Colors.RED}[-] Failed to get user data for account {index}, skipping...{Colors.RESET}")
                    continue

                self.display_user_info(user_data)
                
                # Process tasks
                self.process_tasks(user_data, jwt_token)
                self.process_main_tasks(user_data, jwt_token)
                
                # Add delay between accounts
                if index < len(tokens):
                    delay = 5  # 5 seconds delay between accounts
                    print(f"\n{Colors.YELLOW}[+] Waiting {delay} seconds before processing next account...{Colors.RESET}")
                    time.sleep(delay)

            print(f"\n{Colors.GREEN}=== All accounts processed successfully! ==={Colors.RESET}")
            
            # Calculate and wait for 2 hours
            end_time = datetime.now()
            next_run = end_time + timedelta(hours=2)
            wait_time = (next_run - end_time).total_seconds()
            
            print(f"\n{Colors.YELLOW}[+] Current time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"[+] Next run scheduled for: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"[+] Waiting {int(wait_time/60)} minutes before next cycle...{Colors.RESET}")
            
            try:
                time.sleep(wait_time)
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}[!] Bot stopped by user{Colors.RESET}")
                break

def main():
    try:
        bot = FarDog()
        bot.start()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[!] Bot stopped by user{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}[-] An error occurred: {str(e)}{Colors.RESET}")

if __name__ == "__main__":
    main()
