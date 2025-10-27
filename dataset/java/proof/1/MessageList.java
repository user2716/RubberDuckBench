import java.util.List;

public class MessageList {

    private Preferences preferences;

    private K9Drawer drawer;
    private TextView actionBarSubTitle;
    private LocalSearch search;
    private boolean singleFolderMode;
    private boolean singleAccountMode;
    private boolean drawerEnabled;

    public MessageList(boolean drawerEnabled, int numAccounts) {
        this.preferences = new Preferences(numAccounts);
        this.drawerEnabled = drawerEnabled;
        this.actionBarSubTitle = new TextView();

        if (!isDrawerEnabled()) {
            return;
        }

        this.drawer = new K9Drawer();
    }

    private boolean isDrawerEnabled() {
        return drawerEnabled; 
    }

    public void openFolder(String folderName) {
        LocalSearch search = new LocalSearch(folderName);
        //search.addAccountUuid(account.getUuid());
        //search.addAllowedFolder(folderName);

        performSearch(search);
    }

    private void performSearch(LocalSearch search) {
        initializeFromLocalSearch(search);
    }


    private void initializeFromLocalSearch(LocalSearch search) {
        this.search = search;

        if (search.searchAllAccounts()) {
            List<Account> accounts = preferences.getAccounts();
            singleAccountMode = (accounts.size() == 1);
        } else {
            String[] accountUuids = search.getAccountUuids();
            singleAccountMode = (accountUuids.length == 1);
        }

        List<String> folderServerIds = search.getFolderServerIds();
        singleFolderMode = singleAccountMode && folderServerIds.size() == 1;

        System.out.println("\tNull drawer?: " + (drawer == null));
        System.out.println("\tValue of singleFolderMode: " + singleFolderMode);

        if (drawer == null) {
            return;
        } else if (singleFolderMode) {
            drawer.selectFolder(folderServerIds.get(0));
        } else if (search.getId().equals(LocalSearch.UNIFIED_INBOX)) {
            drawer.selectUnifiedInbox();
        } else {
            drawer.selectFolder(null);
        }

        // now we know if we are in single account mode and need a subtitle
        actionBarSubTitle.setVisibility((!singleFolderMode) ? View.GONE : View.VISIBLE); //Line in quesiton, is this related to drawer?
    }

}
