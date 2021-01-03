package war.moves;

import war.Player;

public class PewCharge extends Attack implements Resource {
    public PewCharge(Player target) {
        super("PewCharge", new Resources[]{}, target);
    }

    @Override
    public int damageOf() {
        return 1;
    }

    @Override
    public Resources[] resources() {
        return new Resources[]{ Resources.CHARGE };
    }
}
