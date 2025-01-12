## 1. Biopython 환경설정 ##
#pip install biopython
import Bio
from Bio import Phylo

## 2. 서브트리 생성 함수 ##
def extract_subtree(tree_file, output_file, target_taxa):
    # 트리 파일을 로드
    tree = Phylo.read(tree_file, "newick")

    # 공통 조상 찾기
    common_ancestor = tree.common_ancestor(target_taxa)

    # 서브트리 추출
    subtree = Phylo.BaseTree.Tree(root=common_ancestor)

    # 서브트리 저장
    Phylo.write(subtree, output_file, "newick")

## 3. 파일 위치 설정 ##
tree_file = 'input/test_itol.tree'
output_file = 'output/test_subtree.nwk'

## 4. 서브트리 시작, 위치 설정 ##
# target_taxa = ['시작 어세션 넘버', '끝 어세션 넘버']
target_taxa = ['GB_GCA_002482885.1', 'RS_GCF_900101855.1'] 

## 5. 서브트리 생성 ##
extract_subtree(tree_file, output_file, target_taxa)