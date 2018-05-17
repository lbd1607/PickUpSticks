#Laura Davis 27 June 2017

#Lesson and source code from YouTube user Trevor Payne
#This program demonstrates the Min Max (Minimax or MM) algorithm in Python.
#This algorithm works best for "perfect information" games, meaning that all possible
#moves and outcomes can be known. Such games include chess and checkers.
#Win/Lose states are represented as +/- infinity. The algorithm solves for the best
#possible move for each player. In 2P games, human is represented as + and computer as -.
#The algorithm works by generating a tree of all possible moves. Each node of the tree
#hold a Heuristic value, which is the state of the game in a single value (this keeps track
#of who is winning and is represented by + or - infinity). Finally, the algorithm then starts with
#from the bottom of the tree and decides the best move for a player after removing all of the
#bad moves first (This is basically a reverse of sorts of the A* algorithm).
#The game here is Pickup Sticks. 
#Coder cheat code solutions: [2, 1, 1, 1] : [1, 2, 1, 1] 

from sys import maxsize
import sys

def main():

##====================================================================================================
##TREE BUILDER
#This section builds the tree of possible moves to be sorted

	class Node(object):
		def __init__(self, i_depth, i_playerNum, i_sticksRemaining, i_value = 0):
			self.i_depth = i_depth
			self.i_playerNum = i_playerNum
			self.i_sticksRemaining = i_sticksRemaining
			self.i_value = i_value
			self.children = []
			self.CreateChildren()
			
		def CreateChildren(self):
			if self.i_depth >= 0:
				for i in range(1, 3):
					v = self.i_sticksRemaining - i
					self.children.append(Node(self.i_depth - 1, 
										-self.i_playerNum, v, self.RealVal(v)))
		
	#determines the value of the game
		def RealVal(self, value):
			if(value == 0):
				return maxsize * self.i_playerNum
			elif(value < 0):
				return maxsize * -self.i_playerNum
			return 0
				
##====================================================================================================
##ALGORITHM
#This is the computational and mathematical portion of the program 

	def	MinMax(node, i_depth, i_playerNum):
		if(i_depth == 0) or (abs(node.i_value) == maxsize):
			return node.i_value
			
		i_bestValue = maxsize * -i_playerNum
		
		for i in range(len(node.children)):
			child = node.children[i]
			i_val = MinMax(child, i_depth - 1, -i_playerNum)
			if (abs(maxsize * i_playerNum -i_val)<
					abs(maxsize * i_playerNum -i_bestValue)):
				i_bestValue = i_val
				
				#DEBUG
				#print i_bestValue
	
		return i_bestValue
		
##====================================================================================================
##ALPHA-BETA PRUNING METHOD
#The alpha-beta pruning method makes the minimax algorithm run more efficiently, thereby
#resulting in harder to beat CPU players

	def alphaBeta(Node, i_depth, alpha, beta, maxedPlayer):
		if (i_depth == 0) or (node ==  maxsize):
			return i_bestValue
		if maxedPlayer:
			v = -maxsize
			for i in range(len(node.children)):
				child = node.children[i]
				v = max(v, alphaBeta(child, i_depth - 1, alpha, beta, False))
				alpha = max(alpha, v)
				if beta <= alpha:
				
				#DEBUG
				#	print(" ")
				#	print ("alpha")
					break
				
			#print ("Value chosen %d") %v
			#print(" ")
			return v
		else:
			v = maxsize
			for i in range(len(node.children)):
				child = node.children[i]
				v = min(v, alphaBeta(child, i_depth - 1, alpha, beta, True))
				beta = min(beta, v)
				if beta <= alpha:
				#DEBUG
				#	print(" ")
				#	print ("beta")
					break

			#print ("Value chosen %d") %v
			#print(" ")
			return v
			

##====================================================================================================
##IMPLEMENTATION
#

	#Checks win or lose
	def WinCheck(i_sticks, i_playerNum):
		if i_sticks <=0:
			print("*" * 60)
			if i_playerNum > 0:
				if i_sticks == 0:
					print ("\tYou WIN!")
				else:
					print ("\tToo many! You lose... ")
			else:
				if i_sticks == 0:
					print ("\tCPU Wins... Better luck next time. ")
				else:
					print ("\tCPU ERROR!")
			print("*" * 60)
			return 0
		return 1

	#Calls the function
	if __name__ == '__main__':
		i_stickTotal = 11
		i_depth = 4
		i_curPlayer = 1
		print("INSTRUCTIONS: Be the player to pick up the last stick." +
		"\nYou can only pick up one(1) or two(2) sticks at a time. ")
		
		#The main code of the game, calls WinCheck, checks input, and increments/decrements
		while (i_stickTotal > 0):
		
			#Checks to ensure that player inputs num between 1 and 2
			#Otherwise, player can enter exact number remaining and
			#win automatically. This process must be contained
			#in a try loop, otherwise Python reads numbers like 11 or 111
			#as 1 and the player is able to cheat. The if-else check WILL NOT
			#work properly without the try loop. The loop also requires a break
			#statement to continue playing the game. If the player inputs any 
			#number other than 1 or 2, the player is called a cheater and the
			#game automatically exits. However, an accidental Return w/o input
			#will not cause exit and the game will continue. The true test will
			#be using this method in larger games, such as checkers or chess.
			while True:
				try:
					print("\n%d sticks remain. How many would you like to pick up?" %i_stickTotal)
					i_choice = int(raw_input("\n1 or 2: "))
				except ValueError:
						print ("Cheater! :P")
				else:
					if 1 <= i_choice <= 3:
						break
					else:
						print ("Cheater! :P ")
						sys.exit(1)	
			i_stickTotal -= int(float(i_choice))
			if WinCheck(i_stickTotal, i_curPlayer):
				i_curPlayer *= -1
				node = Node(i_depth, i_curPlayer, i_stickTotal)
				bestChoice = -100
				i_bestValue = -i_curPlayer * maxsize
				
				#Determine number of sticks to remove
				for i in range(len(node.children)):
					n_child = node.children[i]
					i_val = MinMax(n_child, i_depth, -i_curPlayer)
					if(abs(i_curPlayer * maxsize -i_val) <= 
						abs(i_curPlayer * maxsize -i_bestValue)):
						i_bestValue = i_val
						bestChoice = i
						
				alphaBeta(Node, i_depth, -maxsize, maxsize, True)
	
				bestChoice += 1
				print ("CPU chooses: " + str(bestChoice) + 
						"\tBased on value: " + str(i_bestValue))
				i_stickTotal -= bestChoice
				WinCheck(i_stickTotal, i_curPlayer)
				i_curPlayer *= -1
				
	#Loops the game to play again
	playAgain = raw_input("Would you like to play again? y/n\n")
	if playAgain == ("y"):
		main()
	elif playAgain == ("n"):
		sys.exit(1)
		playAgain = raw_input("Not a valid answer. Would you like to play again? y/n\n ")

main()	
				
