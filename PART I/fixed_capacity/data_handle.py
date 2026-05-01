import pandas as pd
import numpy as np

# 1. 加载你下载的四个 CSV 文件
files = ["CH_d).csv", "DE_d).csv", "FR_d).csv", "AT_d).csv"]
dfs = [pd.read_csv(f) for f in files]
df_all = pd.concat(dfs, ignore_index=True)

# 2. 清理数据：把 'n/e' 替换成空值，并强制转换为数字格式
df_all["Physical Flow (MW)"] = pd.to_numeric(
    df_all["Physical Flow (MW)"].replace('n/e', np.nan), 
    errors='coerce'
)

# 3. 统一国家/竞价区的命名（把复杂的 BZN 映射为标准的两个字母缩写）
country_map = {
    'BZN|CH': 'CH', 'Switzerland (CH)': 'CH',
    'BZN|AT': 'AT', 'Austria (AT)': 'AT',
    'Germany (DE)': 'DE', 'BZN|DE-LU': 'DE', 'BZN|DE-AT-LU': 'DE',
    'BZN|FR': 'FR', 'France (FR)': 'FR'
}
df_all['Out'] = df_all['Out Area'].map(country_map)
df_all['In'] = df_all['In Area'].map(country_map)

# 4. 过滤数据：剔除无关国家，并排除国内的物理流动 (Out == In)
df_filtered = df_all.dropna(subset=['Out', 'In'])
df_filtered = df_filtered[df_filtered['Out'] != df_filtered['In']]

# 5. 创建无向的边界对标识（例如无论方向是 FR->DE 还是 DE->FR，都统一记为 DE-FR）
def make_pair(row):
    pair = sorted([row['Out'], row['In']])
    return f"{pair[0]}-{pair[1]}"

df_filtered['Pair'] = df_filtered.apply(make_pair, axis=1)

# 6. 分组找出每条跨境连线全年的最大物理潮流
max_capacities = df_filtered.groupby('Pair')['Physical Flow (MW)'].max()
print(max_capacities)