package war.moves;

public abstract class Defense extends Move {
    int strength;

    public Defense(String type) {
        super(type);
        strength = strengthOf();
    }

    abstract public int strengthOf();
}
