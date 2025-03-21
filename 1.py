from collections import defaultdict

class Grammar:
    def __init__(self, productions):
        self.productions = productions
        self.non_terminals = set(productions.keys())
        self.first_sets = defaultdict(set)
        self.follow_sets = defaultdict(set)
    
    def compute_first(self):
        def first(symbol):
            if symbol in self.first_sets:
                return self.first_sets[symbol]
            
            first_set = set()
            if symbol not in self.non_terminals:
                first_set.add(symbol)
                return first_set
            
            for production in self.productions[symbol]:
                for char in production:
                    char_first = first(char)
                    first_set.update(char_first - {'ε'})
                    if 'ε' not in char_first:
                        break
                else:
                    first_set.add('ε')
            
            self.first_sets[symbol] = first_set
            return first_set
        
        for non_terminal in self.non_terminals:
            first(non_terminal)
    
    def compute_follow(self):
        self.follow_sets[next(iter(self.non_terminals))].add('$')
        
        while True:
            updated = False
            
            for non_terminal, productions in self.productions.items():
                for production in productions:
                    follow_temp = self.follow_sets[non_terminal].copy()
                    
                    for i in reversed(range(len(production))):
                        symbol = production[i]
                        
                        if symbol in self.non_terminals:
                            before_update = len(self.follow_sets[symbol])
                            self.follow_sets[symbol].update(follow_temp)
                            
                            if 'ε' in self.first_sets[symbol]:
                                follow_temp.update(self.first_sets[symbol] - {'ε'})
                            else:
                                follow_temp = self.first_sets[symbol]
                            
                            updated |= before_update != len(self.follow_sets[symbol])
                        else:
                            follow_temp = {symbol}
            
            if not updated:
                break
    
    def print_follow_sets(self):
        for non_terminal, follow_set in self.follow_sets.items():
            print(f"FOLLOW({non_terminal}): {follow_set}")

productions = {
    'S': ['ACB', 'Cbb', 'Ba'],
    'A': ['da', 'BC'],
    'B': ['g', 'ε'],
    'C': ['h', 'ε']
}

grammar = Grammar(productions)
grammar.compute_first()
grammar.compute_follow()
grammar.print_follow_sets()
