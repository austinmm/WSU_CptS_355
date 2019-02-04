public class Player {
    private int piecesCleared;
    public void setPiecesCleared(int val){ this.piecesCleared = val; }
    public int getPiecesCleared(){ return this.piecesCleared; }
    public void PieceCleared(){this.piecesCleared++;}
    private int score;
    public void setScore(int val){ this.score = val; }
    public int getScore(){ return this.score; }
}
