"""
井字棋 Tic-tac-toe
"""
import random
import sys


class TictactoeAI:
    """
    井字棋AI
    """

    def __init__(self):
        self.__ttt_ai_dict = dict()  # AI库字典

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
            self.__ttt_ai_dict[key] = list_val

    def get_solution(self, board_key):
        """
        按照局势获取走法
        :param board_key: 局势编码字串
        :return: 走格编号，若无解则返回None
        """
        if board_key not in self.__ttt_ai_dict:
            return None
        solutions = self.__ttt_ai_dict[board_key]
        if solutions is None:
            return None
        if len(solutions) == 0:
            return None
        return int(solutions[random.randint(0, len(solutions) - 1)])

    def remove_wrong_solution(self, board_key, solution):
        """
        移除错误的走法，在输棋后调用
        :param board_key: 局势编码字串
        :param solution: 最后一步走格编号
        """
        solutions = self.__ttt_ai_dict[board_key]
        if str(solution) in solutions:
            solutions.remove(str(solution))
        if len(solutions) == 0:
            del self.__ttt_ai_dict[board_key]

    def save_dict(self, file_name):
        """
        把新的AI写入文件
        """
        ttt_items = []
        for ai_key, ai_list in self.__ttt_ai_dict.items():
            ttt_item = ai_key + ":" + ",".join(ai_list)
            ttt_items.append(ttt_item)
        ttt_ai_fullstr = "|".join(ttt_items)
        with open(file_name, "w") as file:
            file.write(ttt_ai_fullstr)


class TictactoeController:
    """
    井字棋游戏控制器：主要负责游戏逻辑处理和电脑AI调用
    """

    def __init__(self):
        self.__ai = TictactoeAI()
        self.__ai_file_name = "ttt_ai_file.txt"
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
        self.__board_data = [0 for _ in range(9)]
        self.__computer_lose = False
        self.__last_board = None
        self.__last_step = None

    def player_step(self, step_pos):
        """
        玩家走棋
        :return: 走棋状态编码
        """
        if not 1 <= step_pos <= 9:
            return 1
        if self.__board_data[step_pos - 1] != 0:
            return 2
        self.__board_data[step_pos - 1] = 1
        return 0

    def computer_step(self):
        """
        电脑走棋
        """
        record_board = "".join([str(item) for item in self.__board_data])
        ai_step = self.__ai.get_solution(record_board)
        if ai_step is None:
            self.__computer_lose = True  # 如果无棋可走自动判电脑认输
        else:
            self.__board_data[ai_step - 1] = 2
            self.__last_board = record_board
            self.__last_step = ai_step

    def check_result(self):
        """
        判定结果
        :return: 2=电脑赢，1=玩家赢，0=继续走，-1=平局
        """
        result = 0
        if self.__computer_lose:
            result = 1  # 电脑认输的时候自动判玩家赢
        else:
            check_str_list = [
                "".join([str(self.__board_data[i]) for i in range(len(self.__board_data)) if i < 3]),
                "".join([str(self.__board_data[i]) for i in range(len(self.__board_data)) if 3 <= i < 6]),
                "".join([str(self.__board_data[i]) for i in range(len(self.__board_data)) if i >= 6]),
                "".join([str(self.__board_data[i]) for i in range(len(self.__board_data)) if i % 3 == 0]),
                "".join([str(self.__board_data[i]) for i in range(len(self.__board_data)) if i % 3 == 1]),
                "".join([str(self.__board_data[i]) for i in range(len(self.__board_data)) if i % 3 == 2]),
                "".join((str(self.__board_data[0]), str(self.__board_data[4]), str(self.__board_data[8]))),
                "".join((str(self.__board_data[2]), str(self.__board_data[4]), str(self.__board_data[6])))
            ]
            for check_str in check_str_list:
                if check_str == "111":
                    result = 1  # 玩家赢
                    break
                if check_str == "222":
                    result = 2  # 电脑赢
                    break
            """
            若全填满但未决出胜负判平局
            """
            if result not in (1, 2):
                have_zero = False
                for item in self.__board_data:
                    if item == 0:
                        have_zero = True
                if not have_zero:
                    result = -1
            if result == 1:
                self.__computer_lose = True  # 无论玩家赢需要更新AI
        if self.__computer_lose:
            if self.__last_board is not None and self.__last_step is not None:
                self.__ai.remove_wrong_solution(self.__last_board, self.__last_step)  # 移除错误的走棋
        return result


class TictactoeView:
    """
    井字棋游戏视图：主要负责游戏界面输出和处理玩家输入指令请求
    """

    def __init__(self):
        self.__controller = TictactoeController()

    def main(self):
        """
        调用入口
        """
        self.__welcome()
        self.__new_start()
        while True:
            self.__player_turn()
            if self.__check_result():
                continue  # 如果棋局结束必须重启循环
            self.__computer_turn()
            self.__check_result()

    def __welcome(self):
        print("井字棋 Tic-tac-toe")
        print()
        print("请按下列图示走棋：")
        print("1 | 2 | 3")
        print("--+---+--")
        print("4 | 5 | 6")
        print("--+---+--")
        print("7 | 8 | 9")
        print("你是X，我是O，请你先走棋。")
        print()

    def __new_start(self):
        self.__controller.init_board()
        self.__controller.init_ai()

    def __player_turn(self):
        while True:
            pos = input("你走棋：")
            if not pos.isdigit():
                print("请正确输入")
                continue
            test = self.__controller.player_step(int(pos))
            if test == 0:
                break
            elif test == 1:
                print("请正确输入")
            elif test == 2:
                print("此处已走过")

    def __computer_turn(self):
        print("我走棋")
        self.__controller.computer_step()

    def __check_result(self):
        self.__print_board()
        result = self.__controller.check_result()
        if result == 2:
            print("我赢了！")
        if result == 1:
            print("你赢了！")
        if result == -1:
            print("平局")
        print()
        if result != 0:
            ask_reset = input("还想再玩吗（y/N）？")
            if ask_reset == "y" or ask_reset == "Y":
                self.__controller.init_board()
                print()
                return True
            else:
                self.__controller.update_ai()
                sys.exit()

    def __print_board(self):
        patterns = [" ", "X", "O"]
        board_data = self.__controller.board_data
        print("%s | %s | %s" % (patterns[board_data[0]], patterns[board_data[1]], patterns[board_data[2]]))
        print("--+---+--")
        print("%s | %s | %s" % (patterns[board_data[3]], patterns[board_data[4]], patterns[board_data[5]]))
        print("--+---+--")
        print("%s | %s | %s" % (patterns[board_data[6]], patterns[board_data[7]], patterns[board_data[8]]))
