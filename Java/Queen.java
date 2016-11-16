public class Queen {
    
    private int x;
    private int y;
    private boolean conflict;
    
    public Queen(int x, int y, boolean conflict){
	this.x = x;
	this.y = y;
	this.conflict = conflict;
    }
    
    public int getConflicts(Queen[] board, int y){
	int conflicts = 0;
	for (int i = 0; i < board.length; i++){
	    Queen nextQueen = board[i];
	    if (i != this.x){
		int rise = Math.abs(y - nextQueen.getY());
		int run = Math.abs(this.x - nextQueen.getX());
		double slope = ((double) rise) / run;
		if (rise == 0){
		    conflicts++;
		} else if (slope == 1.0){
		    conflicts++;
		}
	    }
	}
	
	return conflicts;
    }
    
    public int leastConflicts(Queen[] board){
	int min;
	int minY;
	if (this.y != 0){
	    min = this.getConflicts(board, 0);
	    minY = board[0].getY(); 
	} else {
	    min = this.getConflicts(board, 1);
	    minY = board[1].getY(); 
	}
	int conflicts;
	for (int i = 0; i < board.length; i++){
	    System.out.println(this.y + " = " + i);
	    if (this.y != i){
		conflicts = this.getConflicts(board, i);
		if (conflicts < min){
		    min = conflicts;
		    minY = i;
		}
	    }
	}
	return minY;
    }
    
    public int getX(){
	return this.x;
    }

    public int getY(){
	return this.y;
    }

    public boolean inConflict(){
	return this.conflict;
    }

    public void setX(int x){
	this.x = x;
    }

    public void setY(int y){
	this.y = y;
    }

    public void setConflict(boolean conflict){
	this.conflict = conflict;
    }

    public String toString(){
	return "["+this.x+","+this.y+"]";
    }
}
