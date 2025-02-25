import json
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('user_manager.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)


class UserManager:
    def __init__(self, filename='users.json'):
        self.filename = filename
        self.logger = logging.getLogger(self.__class__.__name__)
        self.users = self.load_users()

    def load_users(self):
        """从json文件加载用户数据"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data
            except json.JSONDecodeError as e:
                self.logger.error(f"JSON解析失败: {str(e)}", exc_info=True)
                raise ValueError("数据文件损坏，请检查文件内容") from e
        else:
            self.logger.warning(f'用户数据文件 {self.filename} 不存在')
            return []

    def __generate_id(self):
        """自增用户ID"""
        if not self.users:
            return 1
        return max(user['id'] for user in self.users) + 1

    def save_users(self):
        """保存用户到json文件"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.users, f, indent=4, ensure_ascii=False)

        except Exception as e:
            self.logger.error(f"保存数据时发生错误：{str(e)}", exc_info=True)

    def add_user(self, username, phone, email):
        """添加新用户"""
        if self.find_by_username(username):
            self.logger.error(f"添加用户失败，用户名 {username} 已存在")
            raise ValueError("用户名已存在")

        new_user = {
            'id': self.__generate_id(),
            'username': username,
            'phone': phone,
            'email': email,
        }
        self.users.append(new_user)
        self.save_users()
        return new_user

    def delete_user(self, user_id):
        """删除用户"""
        original_count = len(self.users)
        self.users = [user for user in self.users if user['id'] != user_id]
        self.save_users()
        return len(self.users) != original_count

    def update_user(self, user_id, **kwargs):
        """更新用户信息"""
        for user in self.users:
            if user['id'] == user_id:
                valid_keys = {'username', 'phone', 'email'}
                updates = {k: v for k, v in kwargs.items() if k in valid_keys}
                user.update(updates)
                self.save_users()
                return user
            return None

    def find_by_username(self, username):
        """通过用户名查找用户"""
        return next((user for user in self.users if user['username'] == username), None)

    def find_by_id(self, user_id):
        """通过id查找用户"""
        return next((user for user in self.users if user['id'] == user_id), None)

    def list_all_users(self):
        """列出所有用户"""
        return self.users.copy()


if __name__ == '__main__':
    manager = UserManager()

    # 添加用户
    manager.add_user("小刚", '18349839999', 'xxx@qq.com')
    manager.add_user("小红", '15544354354',"xxx@qq.com")
    manager.add_user("小强", '15321312312', "xxx@qq.com")

    # 查询用户
    print(manager.find_by_id(1))
    print(manager.find_by_username("小红"))
    print(manager.find_by_username("小明"))

    # 更新用户
    manager.update_user(1, phone='12312321312', email="xxx@xxx.com")

    # 删除用户
    manager.delete_user(2)

    # 查找所有用户
    print("当前用户:")
    for user in manager.list_all_users():
        print(f'ID: {user["id"]}, 用户名: {user["username"]}, 电话: {user["phone"]}, 邮箱: {user["email"]}')

