#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pre-build Auto Linker
ビルド前に全Markdownファイルの用語を自動リンクに変換
"""

import os
import re
import yaml
import shutil
from typing import Dict, Set

class PreBuildAutoLinker:
    def __init__(self, docs_dir: str = "docs"):
        self.docs_dir = docs_dir
        self.backup_dir = docs_dir + "_backup"
        self.term_mappings = {}
        self.definitions = {}
        self.load_config()
    
    def load_config(self):
        """設定ファイルから用語マッピングと定義を読み込む"""
        # autolinks.ymlから用語マッピングを読み込む
        autolinks_path = "autolinks.yml"
        if os.path.exists(autolinks_path):
            with open(autolinks_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                if 'mappings' in data:
                    for item in data['mappings']:
                        term = item.get('term')
                        path = item.get('path')
                        if term and path:
                            self.term_mappings[term] = path
        
        # _definitions.mdから定義を読み込む
        definitions_path = os.path.join(self.docs_dir, "_definitions.md")
        if os.path.exists(definitions_path):
            with open(definitions_path, 'r', encoding='utf-8') as f:
                content = f.read()
                abbr_pattern = r'\*\[([^\]]+)\]:\s*(.+)'
                matches = re.findall(abbr_pattern, content, re.MULTILINE)
                for term, definition in matches:
                    self.definitions[term] = definition.strip()
    
    def backup_docs(self):
        """docsディレクトリをバックアップ"""
        if os.path.exists(self.backup_dir):
            shutil.rmtree(self.backup_dir)
        shutil.copytree(self.docs_dir, self.backup_dir)
        print(f"📁 バックアップ作成: {self.backup_dir}")
    
    def restore_docs(self):
        """docsディレクトリをバックアップから復元"""
        if os.path.exists(self.backup_dir):
            if os.path.exists(self.docs_dir):
                shutil.rmtree(self.docs_dir)
            shutil.copytree(self.backup_dir, self.docs_dir)
            print(f"📁 復元完了: {self.docs_dir}")
    
    def calculate_relative_path(self, current_file: str, target_path: str) -> str:
        """相対パスを計算"""
        current_dir = os.path.dirname(current_file)
        current_depth = current_dir.replace(self.docs_dir, "").count(os.sep)
        
        if current_depth == 0:
            return target_path
        else:
            return "../" * current_depth + target_path
    
    def process_file(self, file_path: str) -> bool:
        """ファイル内の用語を自動リンクに変換"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            processed_terms: Set[str] = set()
            
            # 各用語をリンクに変換
            for term, target_path in self.term_mappings.items():
                if term in processed_terms:
                    continue
                
                # 既にリンクになっている用語は除外
                if (f'[{term}]' in content or 
                    f'>{term}<' in content or 
                    f'href="{target_path}"' in content):
                    continue
                
                # 用語が文中に存在する場合
                if term in content:
                    relative_path = self.calculate_relative_path(file_path, target_path)
                    
                    # シンプルなMarkdownリンクを生成
                    linked_term = f'[{term}]({relative_path})'
                    
                    # 最初の出現のみリンクに変換
                    content = content.replace(term, linked_term, 1)
                    processed_terms.add(term)
            
            # 内容が変更された場合のみファイルを更新
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                rel_path = os.path.relpath(file_path, self.docs_dir)
                print(f"✅ リンク生成: {rel_path}")
                return True
            else:
                rel_path = os.path.relpath(file_path, self.docs_dir)
                print(f"⚪ 変更なし: {rel_path}")
                return False
                
        except Exception as e:
            print(f"❌ エラー: {file_path} - {e}")
            return False
    
    def process_all_files(self):
        """全Markdownファイルを処理"""
        processed_count = 0
        total_count = 0
        
        for root, dirs, files in os.walk(self.docs_dir):
            for file in files:
                if file.endswith('.md') and not file.startswith('_'):
                    file_path = os.path.join(root, file)
                    total_count += 1
                    if self.process_file(file_path):
                        processed_count += 1
        
        print(f"\n📊 処理結果: {processed_count}/{total_count} ファイルを更新")
        print(f"📝 用語マップ: {len(self.term_mappings)} 個")
        return processed_count > 0

def main():
    print("🔗 ビルド前自動リンク生成を開始...")
    
    linker = PreBuildAutoLinker()
    
    # バックアップ作成
    linker.backup_docs()
    
    try:
        # 自動リンク処理
        changes_made = linker.process_all_files()
        
        if changes_made:
            print("\n✨ 自動リンク生成完了！")
            print("🏗️  MkDocsビルドを実行してください: mkdocs build")
            print("🔄 元に戻すには: python prebuild_linker.py --restore")
        else:
            print("\n💡 変更する用語がありませんでした")
            
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        print("🔄 バックアップから復元中...")
        linker.restore_docs()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--restore":
        print("🔄 バックアップから復元中...")
        linker = PreBuildAutoLinker()
        linker.restore_docs()
        print("✅ 復元完了")
    else:
        main()
