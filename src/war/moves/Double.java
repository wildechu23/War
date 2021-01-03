package war.moves;

public class Double extends Defense implements Resource {
    public Double() {
        super("Double", new Resources[]{Resources.CHARGE, Resources.CHARGE});
    }

    @Override
    public int strengthOf() {
        return 2;
    }

    @Override
    public Resources[] resources() {
        return new Resources[]{Resources.DOUBLE};
    }
}
