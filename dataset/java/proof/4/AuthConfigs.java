import java.util.Objects;

public class AuthConfigs {

    private static Boolean cachingEnabled = null;

    public boolean isCachingEnabled() {
        if (Objects.nonNull(AuthConfigs.cachingEnabled)) {
            return cachingEnabled;
        }
        
        //read from environment
        return toBoolean(System.getProperty("nacos.core.auth.caching.enabled", "true"));
    }

    public boolean toBoolean(String bool) {
        return bool != null && bool.equals("true");
    }
    
}
