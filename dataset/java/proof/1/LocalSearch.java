import java.util.HashSet;
import java.util.Set;
import java.util.List;
import java.util.ArrayList;

public class LocalSearch {

    private String id;
    private Set<String> mAccountUuids = new HashSet<>();
    String ALL_ACCOUNTS = "allAccounts";
    public static final String UNIFIED_INBOX = "unified_inbox";

    public LocalSearch(String name) {}


    public boolean searchAllAccounts() {
        //return (mAccountUuids.isEmpty());
        return true;
    }


    public String getId() {
        return (id == null) ? "" : id;
    }

    public String[] getAccountUuids() {
        if (mAccountUuids.isEmpty()) {
            return new String[] { ALL_ACCOUNTS };
        }

        String[] tmp = new String[mAccountUuids.size()];
        mAccountUuids.toArray(tmp);
        return tmp;
    }

    public List<String> getFolderServerIds() {
        List<String> results = new ArrayList<>();
        results.add(id);
        //randomly add rsults 
        return results;
    }

}
