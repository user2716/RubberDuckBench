import java.util.Collections;
import java.util.HashMap;

public class UidFetchCommand {
    private FetchProfile fetchProfile;
    private HashMap<String, Message> messageMap;
    private Builder builder;

    public void readResponse() {
        FetchBodyCallback callback = null;

        if (fetchProfile != null && messageMap != null) {
            if (fetchProfile.contains(FetchProfile.Item.BODY) || fetchProfile.contains(FetchProfile.Item.BODY_SANE)) {
                callback = new FetchBodyCallback(messageMap);
            }
        } 

    }


    public static class Builder  { 
        UidFetchCommand command;
        Builder builder;

        public Builder() {
            command = new UidFetchCommand();
            builder = this;
        }

        public UidFetchCommand build() { 
            return command;
        }

        //takes a hashmap
        public Builder messageParams(FetchProfile fetchProfile, HashMap<String, Message> messageMap) {
            command.fetchProfile = fetchProfile;
            command.messageMap = messageMap;
            return builder;
        }

    }
}
