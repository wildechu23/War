package war.moves;

public class Block extends Defense implements Resource {
    public Block() {
        super("Block", new Resources[]{});
    }

    @Override
    public int strengthOf() {
        return 1;
    }

    @Override
    public Resources[] resources() {
        return new Resources[]{ Resources.BLOCK };
    }
}
