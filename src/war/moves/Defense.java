package war.moves;

public abstract class Defense extends Move {
    int strength;

    public Defense(String type, Resource.Resources[] cost) {
        super(type, cost);
        strength = strengthOf();
    }

    abstract public int strengthOf();
}
