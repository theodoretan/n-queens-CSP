import java.util.Random;

public class NQueens{

    public static void main(String args[]){

	int n = 10;
	Queen[] board = new Queen[n];
	
	for (int i = 0; i < n; i++){
	    board[i] = new Queen(i,i,true);
	    
	    System.out.print(board[i]);
	}
	System.out.println("");
	
	min_conflicts(board, 100);

	for (int i = 0; i < n; i++){
	    System.out.println(board[i]);
	}
	System.out.println("");
	
    }

    public static Queen[] min_conflicts(Queen[] board, int max_steps){
	for (int i = 0; i < max_steps; i++){
	    if (complete(board)){
		return board;
	    }
	    Queen randQueen = getRandom(board);
	    int yPos = randQueen.leastConflicts(board);
	    System.out.print(yPos);
	    randQueen.setY(yPos);
	    for (int j = 0; j < board.length; j++){
		System.out.print(board[j]);
	    }
	    System.out.println("");
	}
	return null;
    }

    public static Queen getRandom(Queen[] board){
	int rand = new Random().nextInt(board.length);
	while (board[rand].getConflicts(board, board[rand].getY()) == 0){
	    rand = new Random().nextInt(board.length);
	}
	System.out.print("" + rand);
	return board[rand];
    }
    
    public static boolean complete(Queen[] board){
	boolean complete = true;
	for (int i = 0; i < board.length; i++){
	    Queen queen = board[i];
	    if (queen.getConflicts(board, queen.getY()) != 0){
		complete = false;
	    }
	}
	return complete;
    }
}
