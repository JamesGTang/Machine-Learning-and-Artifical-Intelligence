package student_player;

import boardgame.Move;
import boardgame.Player;
import tablut.GreedyTablutPlayer;
import tablut.TablutBoardState;
import tablut.TablutMove;

/**
 * This class provides method that run simulations to find the best cost coeffecients for
 * StudentPlayer class
 * Each coeffecient is between 0 and 1, with the incrementation of 0.1 per step, with a total of ((1-0)/0.04)^4=10000 variations
 * With each variation there will be 100 games, so a total of 100,0000 games will be played for one SWEDE or Muscovite
 * @author jamestang
 *
 */
public class Trainer {
	
	double BASE_INCREMENTER=0.1;
	public static void train_swede_coef() {
		for(double i1=0;i1<1;i1+=0.1) {
			for(double i2=0;i2<1;i2+=0.1) {
				for(double i3=0;i3<1;i3+=0.1) {
					for(double i4=0;i4<1;i4+=0.1) {
						double win=0;
						System.out.println("Optimizer set:"+i1+","+i2+","+i3+","+i4);
						Cost cost_optimizer=new Cost(i1, i2, i3, i4);
						for(int num=0;num<10;num++) {					
							Player swede=new StudentPlayer(cost_optimizer);
							swede.setColor(TablutBoardState.SWEDE);
							Player muscovite=new StudentPlayer(cost_optimizer);
							muscovite.setColor(TablutBoardState.MUSCOVITE);
							Player player = muscovite;
							TablutBoardState b = new TablutBoardState();
							 while (!b.gameOver()) {
						            Move m=player.chooseMove(b);
						            b.processMove((TablutMove) m);
						            player = (player == muscovite) ? swede : muscovite;
						     }
							 if(b.getWinner()==1) {
								 // if swede wins
								 win++;
							 }
						}
						System.out.println("Winning percentage: "+win/10);

					}
				}
			}
		}
	}
	
	public static void train_muscovite_coef() {
		for(double i1=0;i1<1;i1+=0.1) {
			for(double i2=0;i2<1;i2+=0.1) {
				for(double i3=0;i3<1;i3+=0.1) {
					for(double i4=0;i4<1;i4+=0.1) {
						double win=0;
						System.out.println("Optimizer set:"+i1+","+i2+","+i3+","+i4);
						Cost cost_optimizer=new Cost(i1, i2, i3, i4);
						for(int num=0;num<10;num++) {					
							Player swede=new StudentPlayer(cost_optimizer);
							swede.setColor(TablutBoardState.SWEDE);
							Player muscovite=new StudentPlayer(cost_optimizer);
							muscovite.setColor(TablutBoardState.MUSCOVITE);
							Player player = muscovite;
							TablutBoardState b = new TablutBoardState();
							 while (!b.gameOver()) {
						            Move m=player.chooseMove(b);
						            b.processMove((TablutMove) m);
						            player = (player == muscovite) ? swede : muscovite;
						     }
							 if(b.getWinner()==0) {
								 // if muscovite wins
								 win++;
							 }
						}
						System.out.println("Winning percentage: "+win/10);

					}
				}
			}
		}
	}
	
	public static void main(String[] args) {
		System.out.println("Starting Swede");
		train_swede_coef();
		train_muscovite_coef();
	}
}
