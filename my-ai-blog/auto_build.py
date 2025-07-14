#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自動ビルドスクリプト
プリプロセス → ビルド → 復元の一連の処理を自動化
"""

import subprocess
import sys
import os
from prebuild_linker import PreBuildAutoLinker

def run_command(command, description):
    """コマンドを実行"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True, encoding='utf-8')
        print(f"✅ {description}完了")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description}失敗: {e}")
        if e.stdout:
            print("出力:", e.stdout)
        if e.stderr:
            print("エラー:", e.stderr)
        return False

def main():
    print("🚀 自動ビルドプロセスを開始...")
    
    # 1. プリプロセス（自動リンク生成）
    print("\n📝 Step 1: 自動リンク生成")
    linker = PreBuildAutoLinker()
    linker.backup_docs()
    
    try:
        changes_made = linker.process_all_files()
        
        if changes_made:
            print("✅ 自動リンク生成完了")
        else:
            print("💡 リンク対象用語なし")
        
        # 2. MkDocsビルド
        print("\n🏗️  Step 2: MkDocsビルド実行")
        build_success = run_command(
            "python -X utf8 -m mkdocs build",
            "MkDocsビルド"
        )
        
        if build_success:
            print("\n🎉 ビルド成功！")
            print("📁 生成されたサイト: site/")
            
            # サーバー起動オプション
            response = input("\n🌐 開発サーバーを起動しますか？ (y/N): ").strip().lower()
            if response == 'y':
                print("🌐 開発サーバー起動中... (Ctrl+C で停止)")
                run_command("python -X utf8 -m mkdocs serve", "開発サーバー起動")
        else:
            print("\n❌ ビルド失敗")
        
    except Exception as e:
        print(f"\n❌ エラーが発生: {e}")
    
    finally:
        # 3. 復元
        print("\n🔄 Step 3: 元ファイル復元")
        linker.restore_docs()
        print("✅ 復元完了")

if __name__ == "__main__":
    main()
