import java.util.List;
import java.util.ArrayList;

public class Preferences {

    private int numAccounts;

    public Preferences(int num) {
        numAccounts = num;
    }

    public List<Account> getAccounts() {
        List<Account> l = new ArrayList<Account>();
        for (int i=0; i<numAccounts; i++) {
            l.add(new Account());
        }

        return l;
    }

}
