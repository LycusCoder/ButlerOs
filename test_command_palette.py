"""
Test script untuk validasi logic Command Palette tanpa GUI
"""
import json
import os

def test_app_icon_detection():
    """Test icon detection logic"""
    
    def get_app_icon(app_name, app_path):
        """Auto-detect emoji icon based on app name/path"""
        name_lower = app_name.lower()
        path_lower = app_path.lower()
        
        # Browser icons
        if any(x in name_lower or x in path_lower for x in ["chrome", "browser", "firefox", "edge"]):
            return "🌐"
        # Code editors
        elif any(x in name_lower or x in path_lower for x in ["vscode", "code", "vs code", "sublime", "atom", "editor"]):
            return "💻"
        # File explorers
        elif any(x in name_lower or x in path_lower for x in ["explorer", "folder", "file", "finder"]):
            return "📁"
        # Terminal/Command
        elif any(x in name_lower or x in path_lower for x in ["cmd", "terminal", "powershell", "bash", "shell"]):
            return "⚡"
        # Music/Media
        elif any(x in name_lower or x in path_lower for x in ["spotify", "music", "media", "vlc", "player"]):
            return "🎵"
        # Communication
        elif any(x in name_lower or x in path_lower for x in ["discord", "slack", "teams", "zoom", "chat"]):
            return "💬"
        # Default
        else:
            return "🚀"
    
    # Test cases
    test_cases = [
        ("Buka Chrome", "chrome", "🌐"),
        ("VS Code", "code", "💻"),
        ("Folder Proyek", "explorer D:\\Projects", "📁"),
        ("Terminal", "cmd", "⚡"),
        ("Spotify", "spotify", "🎵"),
        ("Discord", "discord", "💬"),
        ("Unknown App", "someapp", "🚀"),
    ]
    
    print("🧪 Testing Icon Detection:")
    print("-" * 50)
    all_passed = True
    
    for name, path, expected in test_cases:
        result = get_app_icon(name, path)
        status = "✅" if result == expected else "❌"
        print(f"{status} {name}: {result} (expected: {expected})")
        if result != expected:
            all_passed = False
    
    print("-" * 50)
    if all_passed:
        print("✅ All icon detection tests passed!")
    else:
        print("❌ Some tests failed!")
    
    return all_passed


def test_filter_logic():
    """Test filtering logic"""
    
    # Sample apps
    all_apps = [
        {"name": "Buka Chrome", "path": "chrome"},
        {"name": "Folder Proyek", "path": "explorer D:\\Projects"},
        {"name": "VS Code", "path": "code"},
        {"name": "Spotify", "path": "spotify"},
    ]
    
    def filter_apps(query, apps):
        """Filter apps by query"""
        query = query.strip().lower()
        if not query:
            return apps.copy()
        return [app for app in apps if query in app["name"].lower()]
    
    # Test cases
    test_cases = [
        ("", 4),  # Empty query = all apps
        ("chr", 1),  # Should match "Chrome"
        ("code", 1),  # Should match "VS Code"
        ("pro", 1),  # Should match "Proyek"
        ("xyz", 0),  # No match
        ("o", 4),  # Matches multiple: Chrome, Folder, Code, Spotify
    ]
    
    print("\n🧪 Testing Filter Logic:")
    print("-" * 50)
    all_passed = True
    
    for query, expected_count in test_cases:
        result = filter_apps(query, all_apps)
        actual_count = len(result)
        status = "✅" if actual_count == expected_count else "❌"
        print(f'{status} Query "{query}": {actual_count} results (expected: {expected_count})')
        if actual_count != expected_count:
            all_passed = False
            print(f"    Matched: {[app['name'] for app in result]}")
    
    print("-" * 50)
    if all_passed:
        print("✅ All filter tests passed!")
    else:
        print("❌ Some tests failed!")
    
    return all_passed


def test_config_loading():
    """Test loading config.json"""
    config_path = os.path.join(os.path.dirname(__file__), "src", "config", "config.json")
    
    print("\n🧪 Testing Config Loading:")
    print("-" * 50)
    
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
        
        apps = config.get("quick_apps", [])
        print(f"✅ Config loaded successfully!")
        print(f"✅ Found {len(apps)} apps in config")
        
        for app in apps:
            print(f"   • {app['name']} → {app['path']}")
        
        return True
    except FileNotFoundError:
        print(f"❌ Config file not found: {config_path}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        return False


def main():
    print("=" * 50)
    print("🚀 COMMAND PALETTE - LOGIC VALIDATION")
    print("=" * 50)
    
    # Run all tests
    test1 = test_app_icon_detection()
    test2 = test_filter_logic()
    test3 = test_config_loading()
    
    print("\n" + "=" * 50)
    if all([test1, test2, test3]):
        print("🎉 ALL TESTS PASSED!")
        print("✅ Command Palette logic is working correctly!")
    else:
        print("⚠️ Some tests failed. Please review above.")
    print("=" * 50)


if __name__ == "__main__":
    main()
