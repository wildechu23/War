package war.moves;

public interface Resource {
    Resources[] resources();

    enum Resources {
        CHARGE,
        BLOCK,
        DOUBLE,
        SMOKE,
    }
}
