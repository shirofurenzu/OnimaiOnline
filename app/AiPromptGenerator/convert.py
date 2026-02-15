import yaml
import json
import os

# 設定檔案名稱
input_file = 'zh_TW0.yaml'
output_file = 'data.json'

def convert_yaml_to_flat_json():
    # 檢查檔案是否存在
    if not os.path.exists(input_file):
        print(f"找不到檔案: {input_file}")
        return

    try:
        # 讀取 YAML
        with open(input_file, 'r', encoding='utf-8') as f:
            yaml_data = yaml.safe_load(f)

        if not yaml_data:
            print("YAML 檔案是空的或無法讀取。")
            return

        flat_data = []
        count = 0

        # 遍歷資料結構
        for category_item in yaml_data:
            # === 修正點：加入防呆檢查 ===
            # 如果 category_item 是 None (例如檔案結尾多了一個 -)，直接跳過
            if not category_item:
                continue

            category_name = category_item.get('name', 'Unknown')
            
            # 取得 groups，如果 groups 是 None (有鍵無值)，預設為空列表
            groups = category_item.get('groups') or []
            
            for group_item in groups:
                # === 修正點：加入防呆檢查 ===
                if not group_item:
                    continue

                group_name = group_item.get('name', 'Unknown')
                tags = group_item.get('tags')
                
                # 處理 tags 可能為 None 的情況
                if tags:
                    for tag_en, tag_zh in tags.items():
                        # 建立扁平化物件
                        entry = {
                            "tag": tag_en,
                            "zh": str(tag_zh), # 確保轉為字串
                            "category": category_name,
                            "group": group_name
                        }
                        flat_data.append(entry)
                        count += 1

        # 寫入 JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(flat_data, f, ensure_ascii=False, indent=2)

        print(f"轉換成功！已生成 {output_file}")
        print(f"總共處理了 {count} 個標籤。")

    except Exception as e:
        import traceback
        traceback.print_exc() # 印出詳細錯誤以便除錯
        print(f"\n轉換發生錯誤: {e}")

if __name__ == "__main__":
    convert_yaml_to_flat_json()