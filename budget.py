class Category:

    def __init__(self, category):
        self.category = category
        self.ledger = []

    def __str__(self):
        cat_len = len(self.category)
        max_len = 30
        asterisks = []
        for i in range(max_len - cat_len):
            asterisks.append('*')
        asterisk_index = int(len(asterisks) / 2)
        asterisks.insert(asterisk_index, self.category)
        header = ''.join(asterisks)
        ledger_items = []
        for item in self.ledger:
            ledger_item = []
            whitespace = max_len
            ledger_item.append(item['description'][:23])
            whitespace -= len(ledger_item[0])
            ledger_item.append("{0:.2f}".format(item['amount'])[:7])
            whitespace -= len(ledger_item[1])
            ledger_item.insert(1, ' ' * whitespace)
            ledger_item.append('\n')
            ledger_items.append(ledger_item)
        ledger_lines = ''.join([j for i in ledger_items for j in i])
        total = self.get_balance()
        return f'{header}\n{ledger_lines}Total: {total}'

    def deposit(self, amount, description=''):
        amount = amount
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=''):
        if self.check_funds(amount):
            neg_amount = amount * -1
            self.ledger.append({"amount": neg_amount, "description": description})
            return True
        else:
            return False
    
    def get_balance(self):
        total = 0
        for item in self.ledger:
            total += item['amount']
        return total

    def transfer(self, amount, transfer_category):
        transfer_to_description = 'Transfer to ' + str(transfer_category.category)
        transfer_from_description = 'Transfer from ' + str(self.category)
        if self.check_funds(amount):
            self.withdraw(amount, transfer_to_description)
            transfer_category.deposit(amount, transfer_from_description)
            return True
        else:
            return False

    def check_funds(self, amount):
        balance = self.get_balance()
        if amount > balance:
            return False
        else:
            return True


def create_spend_chart(categories):
    expenses_by_category = []
    total_expenses = 0
    for category in categories:
        category_expenses = []
        total_category_expenses = 0
        category_expenses.append(category.category)
        for item in category.ledger:
            if item['amount'] < 0:
                total_category_expenses += abs(item['amount'])
        category_expenses.append(total_category_expenses)
        total_expenses += total_category_expenses
        expenses_by_category.append(category_expenses)

    def percentage_calculator(x):
        return (x / total_expenses) * 100
    for item in expenses_by_category:
        item[1] = percentage_calculator(item[1])

    # Build y axis and bars
    chart = []
    num_categories = len(expenses_by_category)
    tick = 100
    chart_whitespace = 10
    while tick > -1:
        chart.append(' ' * (3 - len(str(tick))))
        chart.append(tick)
        chart.append('|')
        for item in expenses_by_category:
            if item[1] > tick:
                chart.append(' o ')
            else:
                chart.append(' ' * 3)
            chart_whitespace -= 3
        chart.append(' ' * chart_whitespace)
        chart.append('\n')
        tick -= 10
        chart_whitespace = 10

    # Build x axis labels
    labels = []
    letter_index = 0
    max_len = len(max([item[0] for item in expenses_by_category], key=len))

    for line in range(max_len):
        labels.append(' ' * 4)
        for item in expenses_by_category:
            try:
                labels.append(' ')
                labels.append(item[0][letter_index])
                labels.append(' ')
            except IndexError:
                labels.append(' ' * 2)
        labels.append(' \n')
        letter_index += 1
    labels.pop(-1)
    labels.append('  ')

    # Output builder
    header = 'Percentage spent by category\n'
    chart_lines = ''.join([str(i) for i in chart])
    dashes = ' ' * 4 + '-' + '-' * num_categories * 3 + '\n'
    labels_lines = ''.join([i for i in labels])[:-1]
    return f'{header}{chart_lines}{dashes}{labels_lines}'
