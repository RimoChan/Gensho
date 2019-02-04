import 訊飛


class 節點:
    def __init__(self, 漢字):
        self.漢字 = 漢字
        self.關係 = {}

    def __repr__(self):
        if self.關係:
            return f'({self.漢字}<-{self.關係})'
        else:
            return f'({self.漢字})'

    def 展開(self, 是函數=False):
        if not self.關係:
            return self.漢字
        參數 = []

        前前綴 = ''
        前綴 = ''
        後綴 = ''
        for 關係名, 子節點們 in self.關係.items():

            if 關係名 in ('eSupp',):
                是函數 = True
                for 子節點 in 子節點們:
                    前前綴 += f'if {子節點.展開(True)}: '
            elif 關係名 in ('eProg'):
                for 子節點 in 子節點們:
                    後綴 += f'; {子節點.展開()}'
            elif 關係名 in ('eSucc', 'ePurp',):
                for 子節點 in 子節點們:
                    後綴 += f'.{子節點.展開(True)}'

            elif 關係名 in ('rPat',):
                for 子節點 in 子節點們:
                    前綴 += f'{子節點.展開()}.'
            elif 關係名 in ('Agt', 'Poss', 'Aft', 'Exp'):
                是函數 = True
                for 子節點 in 子節點們:
                    前綴 += f'{子節點.展開()}.'

            elif 關係名 in ('Clas',):
                後綴 += ' == '
                for 子節點 in 子節點們:
                    後綴 += f'{子節點.展開()}'

            elif 關係名 in ('Cont', 'Prod', 'Pat', 'Belg', 'Datv', 'Dir', 'Loc'):
                是函數 = True
                for 子節點 in 子節點們:
                    參數.append(f'{子節點.展開()}')

            elif 關係名 in ('eCoo',):
                for 子節點 in 子節點們:
                    後綴 += f',{子節點.展開()}'

            elif 關係名[0] == 'm':
                None

            else:
                print(f'錯過了關係 {關係名}->[{self.漢字}]')

        參數後綴 = ''
        if 是函數:
            參數後綴 = f'({",".join(參數)})'
        return 前前綴 + 前綴 + self.漢字 + 參數後綴 + 後綴


def 融合(text):
    a = 訊飛.分詞(text)
    b = 訊飛.依存分析(text)
    a = [節點(i) for i in a]

    for i in range(len(b)):
        自節點 = a[i]
        連線 = b[i]
        if b[i]['parent'] == -1:
            主節點 = 自節點
            continue
        父節點 = a[連線['parent']]
        if 連線['relate'] not in 父節點.關係:
            父節點.關係[連線['relate']] = []
        父節點.關係[連線['relate']].append(自節點)

    print(主節點)
    print(主節點.展開())


融合('如果你喜欢这个项目，就加星吧。')
