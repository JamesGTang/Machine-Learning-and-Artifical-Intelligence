package student_player;

import java.util.List;
import coordinates.Coord;
import coordinates.Coordinates;
import tablut.TablutBoardState;
import tablut.TablutMove;

/* use an objective function here with randomization considering following factors
 * For both:
 * 1. Can this move takes out an opponent piece
 * 2. Is this move result in opponent being able to take out my piece after my move
 * 3. Is this move saving my piece from being taken out
 * 4. Does this move causing my piece to suicide
 * For SWEDE
 * 1. Does this move move king closer to corner
 * 2. Dose this move knight closer to corner ( breaking barricade )
 * For M:
 * 1. Does this move block the corner ( corner bloakade strategy ) 
 * 2. Does this move trap the white into an area and prevent it  from reaching corner
 * 
*/

public class Cost {
	static int self = 260685449;
	static double coef_isPieceLossable;
	static double coef_isPieceSuicidal;
	static double coef_isPieceCapturable;
	static double coef_isKingCloser;

	/**
	 * The constructor takes in
	 * 
	 * @param coef_isPieceLossable
	 * @param coef_isPieceSuicidal
	 * @param coef_isPieceCapturable
	 * @param coef_isKingCloser
	 */
	public Cost(double coef_isPieceLossable, double coef_isPieceSuicidal, double coef_isPieceCapturable,
			double coef_isKingCloser) {
		Cost.coef_isPieceLossable = coef_isPieceLossable;
		Cost.coef_isPieceSuicidal = coef_isPieceSuicidal;
		Cost.coef_isPieceCapturable = coef_isPieceCapturable;
		Cost.coef_isKingCloser = coef_isKingCloser;
	}

	public double evaluate_cost_swede(TablutMove move, TablutBoardState boardState) {
		double cost;
		int isPieceLossable = 0;
		int isPieceSuicidal = 0;
		int isPieceCapturable = 0;
		int isKingCloser = 0;
		int maxLost = 0;
		int opponent = boardState.getOpponent();
		// clone current boardstate for simulation
		TablutBoardState l1BS = (TablutBoardState) boardState.clone();
		// get the current number of pieces
		int numberofOpponentPiecesl1 = l1BS.getNumberPlayerPieces(opponent);
		int numberofSelfPiecesl1 = l1BS.getNumberPlayerPieces(self);
		// run the first move
		l1BS.processMove(move);
		// can this move take out opponent piece
		if (l1BS.getNumberPlayerPieces(opponent) < numberofOpponentPiecesl1) {
			// if this move takes out another piece
			isPieceCapturable = 1;
		}
		// if this move results in my piece suicidal
		if (l1BS.getNumberPlayerPieces(self) < numberofSelfPiecesl1) {
			isPieceSuicidal = -1;
		}
		// if this move causes the game to be won, indicating by using a strong outlier
		if (l1BS.getWinner() == 1) {
			return 10000;
		}
		// check next level and see if the opponent player is able to take out our piece
		// due to this move
		TablutBoardState l2BS = (TablutBoardState) l1BS.clone();
		List<TablutMove> l2MV = l2BS.getAllLegalMoves();
		for (TablutMove l2mv : l2MV) {
			TablutBoardState l2C1BS = (TablutBoardState) l2BS.clone();
			int l2PC = l2C1BS.getNumberPlayerPieces(self);
			l2C1BS.processMove(l2mv);
			// find out how many ways this move leaves opponent opportunity to capture my
			// move
			int pieceLoss = l2PC - l2C1BS.getNumberPlayerPieces(self);
			if (pieceLoss > 0) {
				isPieceLossable--;
			}
			// find out how many pieces at most will i lost if opponent makes a greedy move
			if (maxLost <= pieceLoss) {
				maxLost = pieceLoss;
			}
		}
		// negate maxLost since its a penalty
		maxLost = -maxLost;
		// playing as swede
		Coord kingPos = boardState.getKingPosition();
		// if the moves king and the king will land on corner,return a strong outlier to
		// make sure the winning move is taken
		if (move.getStartPosition() == kingPos && Coordinates.isCorner(move.getEndPosition())) {
			return 10000;
		}
		int distBefore = Coordinates.distanceToClosestCorner(kingPos);
		TablutBoardState l1C1BS = (TablutBoardState) boardState.clone();
		l1C1BS.processMove(move);
		// if the heuristic manhattan distance for the king is closer after the move
		if (distBefore > Coordinates.distanceToClosestCorner(l1C1BS.getKingPosition())) {
			isKingCloser = distBefore-Coordinates.distanceToClosestCorner(l1C1BS.getKingPosition());
		}
		// if moving king to a closer location causing the opponent kiiling king in next
		// move
		List<TablutMove> l1MV = l1C1BS.getAllLegalMoves();
		for (TablutMove l1mv : l1MV) {
			TablutBoardState l2C2BS = (TablutBoardState) l1C1BS.clone();
			l2C2BS.processMove(l1mv);
			if (l2C2BS.gameOver()) {
				return -9999;
			}
		}
		// ToDo: add cornering situation
		cost = coef_isKingCloser * isKingCloser + coef_isPieceCapturable * isPieceCapturable
				+ coef_isPieceLossable * isPieceLossable + coef_isPieceSuicidal * isPieceSuicidal;

		return cost;
	}

	public double evaluate_cost_muscovite(TablutMove move, TablutBoardState boardState) {
		double cost;
		int isPieceLossable = 0;
		int isPieceSuicidal = 0;
		int isPieceCapturable = 0;
		int isKingCloser = 0;
		int maxLost = 0;
		int opponent = boardState.getOpponent();
		// clone current boardstate for simulation
		TablutBoardState l1BS = (TablutBoardState) boardState.clone();
		// get the current number of pieces
		int numberofOpponentPiecesl1 = l1BS.getNumberPlayerPieces(opponent);
		int numberofSelfPiecesl1 = l1BS.getNumberPlayerPieces(self);
		Coord kingPos = boardState.getKingPosition();
		// run the first move
		l1BS.processMove(move);
		// can this move take out opponent piece
		if (l1BS.getNumberPlayerPieces(opponent) < numberofOpponentPiecesl1) {
			// if this move takes out another piece
			isPieceCapturable = 1;
		}
		// if this move results in my piece suicidal
		if (l1BS.getNumberPlayerPieces(self) < numberofSelfPiecesl1) {
			isPieceSuicidal = -1;
		}
		// if this move causes the game to be won, indicating by using a strong outlier
		if (l1BS.gameOver()) {
			return 10000;
		}
		// due to this move
		TablutBoardState l2BS = (TablutBoardState) l1BS.clone();
		List<TablutMove> l2MV = l2BS.getAllLegalMoves();
		for (TablutMove l2mv : l2MV) {
			TablutBoardState l2C1BS = (TablutBoardState) l2BS.clone();
			int l2PC = l2C1BS.getNumberPlayerPieces(self);
			l2C1BS.processMove(l2mv);
			// find out if the king is able to move to the final postion
			if (move.getStartPosition() == kingPos && Coordinates.isCorner(move.getEndPosition())) {
				System.out.println("Avoid lossing move");
				return -9999;
			}
			// find out how many ways this move leaves opponent opportunity to capture my move
			int pieceLoss = l2PC - l2C1BS.getNumberPlayerPieces(self);
			if (pieceLoss > 0) {
				isPieceLossable--;
			}
			// find out how many pieces at most will i lost if opponent makes a greedy move
			if (maxLost <= pieceLoss) {
				maxLost = pieceLoss;
			}
		}
		// negate maxLost since its a penalty
		maxLost = -maxLost;
		// different cost function for playing as Swede or M
		int distBefore = Coordinates.distanceToClosestCorner(kingPos);
		TablutBoardState l1C2BS = (TablutBoardState) boardState.clone();
		if (distBefore > Coordinates.distanceToClosestCorner(l1C2BS.getKingPosition())) {
			isKingCloser = distBefore-Coordinates.distanceToClosestCorner(l1C2BS.getKingPosition());
		}
		cost = -coef_isKingCloser * isKingCloser + coef_isPieceCapturable * isPieceCapturable
				+ coef_isPieceLossable * isPieceLossable + coef_isPieceSuicidal * isPieceSuicidal;

		return cost;
	}
}
