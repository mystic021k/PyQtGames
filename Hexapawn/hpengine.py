"""
六兵棋 Hexapawn
"""
import random
import sys


class HexapawnAI:
    """
    六兵棋AI
    """

    def __init__(self):
        self.__hp_ai_dict = dict()  # AI库字典

    def read_dict(self, file_name):
        """
        读取文件获取AI库
        """
        with open(file_name, "r") as file:
            text_data = file.read()
        kv_pairs = text_data.split("|")
        for pair in kv_pairs:
            key, list_str_val = pair.split(":")
            list_val = list_str_val.split(",")
            self.__hp_ai_dict[key] = list_val

    def get_solution(self, board_key):
        """
        按照局势获取走法
        :param board_key: 局势编码字串
        :return: 走格编号，若无解则返回None
        """
        if board_key not in self.__hp_ai_dict:
            return None
        solutions = self.__hp_ai_dict[board_key]
        if solutions is None:
            return None
        if len(solutions) == 0:
            return None
        startend = solutions[random.randint(0, len(solutions) - 1)]
        se_arr = startend.split("-")
        return int(se_arr[0]), int(se_arr[1])

    def remove_wrong_solution(self, board_key, start, end):
        """
        移除错误的走法，在输棋后调用
        :param board_key: 局势编码字串
        :param start: 最后一步棋子走格编号
        :param end: 最后一步目标走格编号
        """
        solution = str(start) + "-" + str(end)
        solutions = self.__hp_ai_dict[board_key]
        if solution in solutions:
            solutions.remove(solution)
        if len(solutions) == 0:
            del self.__hp_ai_dict[board_key]

    def save_dict(self, file_name):
        """
        把新的AI写入文件
        """
        hp_items = []
        for ai_key, ai_list in self.__hp_ai_dict.items():
            hp_item = ai_key + ":" + ",".join(ai_list)
            hp_items.append(hp_item)
        hp_ai_fullstr = "|".join(hp_items)
        with open(file_name, "w") as file:
            file.write(hp_ai_fullstr)


class HexapawnController:
    """
    六兵棋游戏控制器：主要负责游戏逻辑处理和电脑AI调用
    """

    def __init__(self):
        self.__ai = HexapawnAI()
        self.__ai_file_name = "hp_ai_file.txt"
        self.__board_data = []
        self.__computer_lose = False
        self.__last_board = None
        self.__last_step = None

    @property
    def board_data(self):
        return self.__board_data

    def init_ai(self):
        """
        初始化AI
        """
        self.__ai.read_dict(self.__ai_file_name)

    def update_ai(self):
        """
        更新AI文件
        """
        self.__ai.save_dict(self.__ai_file_name)

    def init_board(self):
        """
        初始化棋盘
        """
        self.__board_data = [2, 2, 2, 0, 0, 0, 1, 1, 1]
        self.__computer_lose = False
        self.__last_board = None
        self.__last_step = None

    def player_step(self, start_pos, end_pos):
        """
        玩家走棋
        :return: 走棋状态编码
        """
        if (not 1 <= start_pos <= 9) or (not 1 <= end_pos <= 9):
            return 1
        if self.__board_data[start_pos - 1] != 1:
            return 2
        pass_way = False
        if start_pos > 3:
            if end_pos == start_pos - 3 and self.__board_data[end_pos - 1] == 0:
                pass_way = True
            elif self.__board_data[end_pos - 1] == 2 and (
                    end_pos == start_pos - 2 or end_pos == start_pos - 4) and (
                    start_pos - 1) // 3 == (end_pos - 1) // 3 + 1:
                pass_way = True
        if pass_way:
            self.__board_data[start_pos - 1] = 0
            self.__board_data[end_pos - 1] = 1
            return 0
        else:
            return 3

    def computer_step(self):
        """
        电脑走棋
        """
        record_board = "".join([str(item) for item in self.__board_data])
        ai_step = self.__ai.get_solution(record_board)
        if ai_step is None:
            self.__computer_lose = True  # 如果无棋可走自动判电脑认输
        else:
            self.__board_data[ai_step[0] - 1] = 0
            self.__board_data[ai_step[1] - 1] = 2
            self.__last_board = record_board
            self.__last_step = ai_step

    def check_result(self, last_char):
        """
        判定结果
        :return: 2=电脑赢，1=玩家赢，0=继续走
        """
        result = 0
        if self.__computer_lose:
            result = 1  # 电脑认输的时候自动判玩家赢
        else:
            player_left_steps = 0
            computer_left_steps = 0
            for i in range(len(self.__board_data)):
                if i < 3 and self.__board_data[i] == 1:  # 玩家走到末线判赢
                    result = 1
                    break
                if i > 5 and self.__board_data[i] == 2:  # 电脑走到末线判赢
                    result = 2
                    break
                if self.__board_data[i] == 1:  # 确认玩家是否还能走棋
                    if self.__board_data[i - 3] == 0:
                        player_left_steps += 1
                    if ((i % 3 == 0 or i % 3 == 1) and self.__board_data[i - 2] == 2) or (
                            (i % 3 == 1 or i % 3 == 2) and self.__board_data[i - 4] == 2):
                        player_left_steps += 1
                if self.__board_data[i] == 2:  # 确认电脑是否还能走棋
                    if self.__board_data[i + 3] == 0:
                        computer_left_steps += 1
                    if ((i % 3 == 0 or i % 3 == 1) and self.__board_data[i + 4] == 1) or (
                            (i % 3 == 1 or i % 3 == 2) and self.__board_data[i + 2] == 1):
                        computer_left_steps += 1
            if result == 0:  # 如果对方已无棋可走判自己赢
                if last_char == 1 and computer_left_steps == 0:
                    result = 1
                if last_char == 2 and player_left_steps == 0:
                    result = 2
            if result == 1:
                self.__computer_lose = True  # 如果玩家赢需要更新AI
        if self.__computer_lose:
            if self.__last_board is not None and self.__last_step is not None:
                self.__ai.remove_wrong_solution(self.__last_board, self.__last_step[0], self.__last_step[1])  # 移除错误的走棋
        return result


class HexapawnView:
    """
    六兵棋游戏视图：主要负责游戏界面输出和处理玩家输入指令请求
    """

    def __init__(self):
        self.__controller = HexapawnController()

    def main(self):
        """
        调用入口
        """
        self.__welcome()
        self.__new_start()
        while True:
            self.__player_turn()
            if self.__check_result(1):
                continue  # 如果棋局结束必须重启循环
            self.__computer_turn()
            self.__check_result(2)

    def __welcome(self):
        print("六兵棋 Hexapawn")
        print()
        print("请按下列图示走棋：")
        print("1 2 3")
        print("4 5 6")
        print("7 8 9")
        print("你是X，我是O，请你先走棋。")
        print()

    def __new_start(self):
        self.__controller.init_board()
        self.__controller.init_ai()
        self.__print_board()
        print()

    def __player_turn(self):
        print("你走棋")
        while True:
            pos_start = input("移动棋子：")
            pos_end = input("目标位置：")
            if not pos_start.isdigit() or not pos_end.isdigit():
                print("请正确输入")
                continue
            test = self.__controller.player_step(int(pos_start), int(pos_end))
            if test == 0:
                break
            elif test == 1:
                print("请正确输入")
            elif test == 2:
                print("此处无棋子")
            elif test == 3:
                print("走棋错误")

    def __computer_turn(self):
        print("我走棋")
        self.__controller.computer_step()

    def __check_result(self, current_char):
        self.__print_board()
        result = self.__controller.check_result(current_char)
        if result == 2:
            print("我赢了！")
        if result == 1:
            print("你赢了！")
        print()
        if result != 0:
            ask_reset = input("还想再玩吗（y/N）？")
            if ask_reset == "y" or ask_reset == "Y":
                self.__controller.init_board()
                print()
                self.__print_board()
                print()
                return True
            else:
                self.__controller.update_ai()
                sys.exit()

    def __print_board(self):
        patterns = [".", "X", "O"]
        board_data = self.__controller.board_data
        print("%s %s %s" % (patterns[board_data[0]], patterns[board_data[1]], patterns[board_data[2]]))
        print("%s %s %s" % (patterns[board_data[3]], patterns[board_data[4]], patterns[board_data[5]]))
        print("%s %s %s" % (patterns[board_data[6]], patterns[board_data[7]], patterns[board_data[8]]))
