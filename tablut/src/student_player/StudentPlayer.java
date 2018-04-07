package student_player;

import java.util.List;
import boardgame.Move;
import boardgame.Player;
import tablut.GreedyTablutPlayer;
import tablut.TablutBoardState;
import tablut.TablutMove;
import tablut.TablutPlayer;

/** A player file submitted by a student. */
public class StudentPlayer extends TablutPlayer {
	long startTime;
	int self=260685449;
	int opponent;
	Cost cost_optimizer;
	/**
	 * Default constructor
	 */
    public StudentPlayer() {
        super("260685449");
        
    }
    /**
     * This constructor is used for training only
     * @param cost_optimizer overrides the in class constrcutor with experimental values
     */
    public StudentPlayer(Cost cost_optimizer) {
    	this.cost_optimizer=cost_optimizer;
    }

    /**
     * This is the primary method that you need to implement. The ``boardState``
     * object contains the current state of the game, which your agent must use to
     * make decisions.
     */
    public Move chooseMove(TablutBoardState boardState) {
    	
    	if(TablutBoardState.SWEDE==boardState.getOpponent()) {
    		cost_optimizer=new Cost(0.35, 0.45, 1, 0.5);
    	}else {
    		cost_optimizer=new Cost(0.14, 0.225, 0.2, 1);
    	}
    	// keep tracks of the each move's time
    	startTime=System.currentTimeMillis();
    	opponent=boardState.getOpponent();
    	double maxGain=-999;
    	boolean isPlayerSwede;
    	TablutMove bestMove=(TablutMove)boardState.getRandomMove();
    	// find if player is swede or not
    	if (player_id==TablutBoardState.SWEDE) isPlayerSwede=true;
    	else isPlayerSwede=false;
    	
    	List<TablutMove> l0Mv = boardState.getAllLegalMoves();   	
        // for every move in the possible moves
    	//System.out.println("Move: "+boardState.getTurnNumber());
    	for(TablutMove maxMove1:l0Mv) {
    		double cost;
    		// if i am playing M	
    		if(TablutBoardState.SWEDE==boardState.getOpponent()) {
    			cost=cost_optimizer.evaluate_cost_muscovite(maxMove1, boardState);
    		}else {
    			// i am playing swede
    			cost=cost_optimizer.evaluate_cost_swede(maxMove1,boardState);
    		}
    		//System.out.println("Cost is: "+cost);
    		// store equal cost moves in the data structure
    		if(maxGain<cost) {
    			maxGain=cost;
    			bestMove=maxMove1;
    		}
    	}
    	//System.out.println("l1,l2,l3: "+l1+" "+l2+" "+l3);
    	//System.out.println("Choosign move with gain: "+maxGain);
    	//System.out.println("Time usage for move: "+(System.currentTimeMillis()-startTime)/1000);
        // Return your move to be processed by the server.
        return bestMove;
    }
    
    public static void main(String[] args) {
    	System.out.println("Testing student player");
    	TablutBoardState b = new TablutBoardState();
    	Player swede = new GreedyTablutPlayer();
        swede.setColor(TablutBoardState.SWEDE);
        Player musovite=new StudentPlayer();
        musovite.setColor(TablutBoardState.MUSCOVITE);
        Player player = musovite;
        while (!b.gameOver()) {
            Move m = player.chooseMove(b);
            b.processMove((TablutMove) m);
            player = (player == musovite) ? swede : musovite;
            System.out.println("\nMOVE PLAYED: " + m.toPrettyString());
            //b.printBoard();
        }
        System.out.println(TablutMove.getPlayerName(b.getWinner()) + " WIN!");
    }
    
}