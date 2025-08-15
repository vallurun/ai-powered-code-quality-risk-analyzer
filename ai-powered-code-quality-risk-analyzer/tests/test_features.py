from src.feature_extractor import featureize

def test_featureize_counts():
    patch = '''diff --git a/x.py b/x.py
index 83db48a..bf12f9a 100644
--- a/x.py
+++ b/x.py
@@ -1,3 +1,3 @@
-print("old")
+print("new")
'''
    feats = featureize(patch)
    assert feats["num_files"] >= 1
    assert feats["lines_added"] >= 1
