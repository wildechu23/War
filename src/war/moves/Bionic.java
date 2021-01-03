package war.moves;

public class Bionic extends Defense implements Resource {
    public Bionic() {
        super("Bionic", new Resources[]{Resources.CHARGE, Resources.CHARGE, Resources.CHARGE, Resources.CHARGE});
    }

    @Override
    public int strengthOf() {
        return 4;
    }

    @Override
    public Resources[] resources() {
        return new Resources[]{Resources.DOUBLE, Resources.DOUBLE};
    }
}
