import pandas as pd
import numpy as np


data = pd.read_csv('/Users/natalienie/Desktop/FS.csv')
choice = data['choice'].tolist()
sales = [10000, 2000, 4000, -2000, -1000, 5769, 2465, 1622, 4640, 0, 1101]
costs = data['cost_of_sales'].tolist()
Delta_AR = data['Delta_AR'].tolist()
Delta_AP = data['Delta_AP'].tolist()
Delta_Inventory = data['Delta_Inventory'].tolist()
P1_choices = choice[1:5]
P2_choices = choice[5:8]
P3_choices = choice[8:]
P1_sales = sales[1:5]
P2_sales = sales[5:8]
P3_sales = sales[8:]
P1_costs = costs[1:5]
P2_costs = costs[5:8]
P3_costs = costs[8:]
P1_Delta_AR = Delta_AR[1:5]
P2_Delta_AR = Delta_AR[5:8]
P3_Delta_AR = Delta_AR[8:]
P1_Delta_AP = Delta_AP[1:5]
P2_Delta_AP = Delta_AP[5:8]
P3_Delta_AP = Delta_AP[8:]
P1_Delta_Inventory = Delta_Inventory[1:5]
P2_Delta_Inventory = Delta_Inventory[5:8]
P3_Delta_Inventory = Delta_Inventory[8:]
start_credit = 2844
start_inventory = 2305
start_AR = 3014
start_AP = 1050
start_sales = 10000
start_cost = 9350
interest = 0.08
tax = 0.4
start_CCC = 156
start_FCF = 260
start_net_income = 236
credit_line = 3200
start_EBIT = 650
"""

"""

class Choice(object):



    def __init__(self, choice, change_inventory, change_sales, change_cost, change_AR, change_AP):


        self.choice = choice
        self.change_inventory = change_inventory
        self.change_sales = change_sales
        self.change_cost = change_cost
        self.change_AR = change_AR
        self.change_AP = change_AP
        self.FCF = (self.change_sales - self.change_cost)*(1-tax)
        """
        self.change_income = (self.change_sales - self.change_cost - change_delta_credit_line_by * 0.08) * (1-tax)
        self.delta_credit_line_by = self.change_inventory + self.change_AR - self.change_AP - self.change_income
        """

        self.change_income = self.EBIT*0.6
        self.change_credit_line = self.change_income + self.change_AP - self.change_AR - self.change_inventory
        """
        self.change_income = 0.6302*(self.change_sales-self.change_cost) - 0.0504*(self.change_inventory + self.change_AR+self.change_AP)
        self.change_credit_line = 1.05042*(self.change_inventory + self.change_AR - self.change_AP) - 0.63025*(self.change_cost - self.change_sales)
        """


        self.CCC = (start_inventory + self.change_inventory - start_AP - self.change_AP)*365/(start_cost + self.change_cost) + 365*(start_AR + self.change_AR)/(start_sales + self.change_sales)
        self.delta_CCC = self.CCC - 156

        self.credit_used = start_credit + self.change_credit_line

    def get_Name(self):

        return self.choice

    def get_sales(self):

        return self.change_sales

    def getInv(self):

        return self.change_inventory

    def get_AR(self):

        return self.change_AR

    def get_AP(self):

        return self.change_AP

    def get_cost(self):

        return self.change_cost

    def getCCC():

        return self.delta_CCC

    def get_credit_line(self):

        return self.change_credit_line

    def getFCF(self):

        return self.FCF

    def getCapitalReturn(self):
        return self.FCF / self.change_credit_line

    def get_change_income(self):
        return self.change_income



def buildMatrix(choices, sales, costs, inventories, AR, AP):
    matrix = []
    for i in range(len(choices)):
        matrix.append(Choice(choices[i], inventories[i], sales[i], costs[i], AR[i], AP[i]))
    return matrix


def optimize(matrix, constraint, keyFunction, reverse = True ):

        matrixCopy = sorted(matrix, key = keyFunction, reverse = reverse)
        result = []
        totalCredit = start_credit
        maxCredit = credit_line
        cashflow = 260
        net_income = start_net_income
        total_Capital_return = cashflow / totalCredit
        EBIT = start_EBIT
        """
        global start_inventory
        global start_AP
        global start_AR
        global start_sales
        global start_cost
        global start_FCF
        """

        for i in range(len(matrixCopy)):
            x = totalCredit+matrixCopy[i].get_credit_line()
            if x <= constraint:
                result.append(matrixCopy[i].get_Name())
                totalCredit += matrixCopy[i].get_credit_line()
                #Capital_return.append(matrixCopy[i].Capital_return())
                net_income_changed = start_net_income + matrixCopy[i].get_change_income()
                net_income = net_income_changed
                totalCredit += matrixCopy[i].get_credit_line()
                FCF_changed = (EBIT + matrixCopy[i].get_sales() - matrixCopy[i].get_cost()) * 0.6
                cashflow = FCF_changed
                changed_inv = start_inventory + matrixCopy[i].getInv()
                changed_AP = start_AP + matrixCopy[i].get_AP()
                changed_AR = start_AR + matrixCopy[i].get_AR()
                changed_sales = start_sales + matrixCopy[i].get_sales()
                changed_cost = start_cost + matrixCopy[i].get_cost()
                CCC_changed = 365*(changed_inv - changed_AP)/changed_cost + 365*changed_AR/changed_sales
                CapitalReturn = cashflow / totalCredit

        print('choices picked for this phase {}'.format(result))
        print('FCF value is now {}'.format(cashflow))
        print('Net income is now {}'.format(net_income))
        print('CCC is now {} days'.format(CCC_changed))
        print('CapitalReturn is now {}'.format(CapitalReturn))
