package war.moves;

public class Charge extends Defense implements Resource {
    public Charge() {
        super("Charge");
    }

    @Override
    public int strengthOf() {
        return 0;
    }

    @Override
    public Resources[] resources() {
        return new Resources[]{ Resources.CHARGE };
    }
}
