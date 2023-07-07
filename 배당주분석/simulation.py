

#주식 거래 시뮬레이션 클래스
class Account:

    #거래정보이력
    TRADE_HISTORY = []

    class trade:
        def __init__(self, code:str, price:int, quantity:int, type:str,date:str):
            self.code = code
            self.price = price
            self.quantity = quantity
            self.type = type
            self.date = date

        def get_trade(self):
            return self.__dict__

    STOCK = {
            'code': '',
            'price': 0,
            'quantity': 0,
        }
    FEE = 0.0025 #수수료 0.25%
    DIV_TAX = 0.154 #세금 15%   
    DATE = ''
    #생성자
    def __init__(self,init_money:int):
        self.account = {
            'balance': init_money,
            'stocks': [],
        }

    def set_date(self,date:str):
        self.DATE = date
    
    #거래이력 추가
    def add_trade_history(self, code:str, price:int, quantity:int, type:str):
        self.TRADE_HISTORY.append(self.trade(code,price,quantity,type,self.DATE))


    #매수가능 수량 조회
    def get_buyable_quantity(self, price:int):
        acc = self.get_account()
        if acc['balance'] == 0:
            return 0
        return int(acc['balance'] / (price * (1+self.FEE)))
    
    def get_sellable_quantity(self, code:str):
        acc = self.get_account()
        for stock in acc['stocks']:
            if stock['code'] == code:
                return stock['quantity']

    def get_account(self):
        #잔여 수량 0인 주식 삭제
        for stock in self.account['stocks']:
            if stock['quantity'] == 0:
                self.account['stocks'].remove(stock)

        return self.account

    def buy(self, code:str,price:int,quantity:int):
        """
        매수
        매수할 주식이 이미 계좌에 있는지 확인
        있으면 매수할 주식의 수량만 증가
        없으면 계좌에 주식 추가
        매수할 주식의 가격만큼 계좌의 잔고 감소
        매수할 주식의 수량만큼 계좌의 주식 수량 증가
        매수할 주식의 종목코드, 종목명, 가격, 수량을 계좌의 주식에 추가
        """
        if quantity == 0:
            return False
        if self.account['balance'] < price * quantity * (1+self.FEE):
            return False
        
        add_balance = price * quantity * (1 + self.FEE)
        
        isin = False
        for stock in self.account['stocks']:
            if stock['code'] == code:
                stock['quantity'] += quantity
                isin = True
                
        if not isin:
            self.account['stocks'].append({
                'code': code,
                'price': price,
                'quantity': quantity,
            })

        self.account['balance'] -= add_balance
        self.add_trade_history(code,price,quantity,'buy')
        return True
    
    def sell(self, code:str,price:int,quantity:int):
        """
        매도
        매도할 주식이 계좌에 있는지 확인
        있으면 매도할 주식의 수량만큼 계좌의 주식 수량 감소
        없으면 매도할 주식이 없다고 출력
        매도할 주식의 가격만큼 계좌의 잔고 증가
        매도할 주식의 종목코드, 종목명, 가격, 수량을 계좌의 주식에서 삭제
        """
        if quantity == 0:
            return False


        add_balance = price * quantity * (1 - self.FEE)

        for stock in self.account['stocks']:
            if stock['code'] == code:
                if stock['quantity'] < quantity:
                    return False
                stock['quantity'] -= quantity
                self.account['balance'] += add_balance
                self.add_trade_history(code,price,quantity,'sell')
                return True
            
        return False
    
    #배당금 입금
    def get_dividends(self, code:str,div_price:int):
        acc = self.get_account()
        add_balance = 0
        for stock in acc['stocks']:
            if stock['code'] == code:
                add_balance = div_price * stock['quantity'] * (1 - self.DIV_TAX)

        self.account['balance'] += add_balance

        self.add_trade_history(code,add_balance,0,'dividends')

        return add_balance

        

