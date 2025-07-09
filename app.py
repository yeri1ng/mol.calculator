import re
import streamlit as st

# 1. 화학식 파싱 함수
def parse_formula(formula):
    tokens = re.findall(r'([A-Z][a-z]?|\(|\)|\d+)', formula)
    stack = [{}]

    i = 0
    while i < len(tokens):
        token = tokens[i]

        if token == '(':
            stack.append({})
            i += 1
        elif token == ')':
            group = stack.pop()
            i += 1
            count = 1
            if i < len(tokens) and tokens[i].isdigit():
                count = int(tokens[i])
                i += 1
            for elem, num in group.items():
                stack[-1][elem] = stack[-1].get(elem, 0) + num * count
        elif re.match(r'[A-Z][a-z]?$', token):
            elem = token
            i += 1
            count = 1
            if i < len(tokens) and tokens[i].isdigit():
                count = int(tokens[i])
                i += 1
            stack[-1][elem] = stack[-1].get(elem, 0) + count
        else:
            i += 1

    return stack.pop()

# 2. 원자량 데이터
atomic_weights = {
    'H': 1.008,
    'He': 4.0026,
    'Li': 6.94,
    'Be': 9.0122,
    'B': 10.81,
    'C': 12.011,
    'N': 14.007,
    'O': 15.999,
    'F': 18.998,
    'Ne': 20.180,
    'Na': 22.990,
    'Mg': 24.305,
    'Al': 26.982,
    'Si': 28.085,
    'P': 30.974,
    'S': 32.06,
    'Cl': 35.45,
    'Ar': 39.948,
    'K': 39.098,
    'Ca': 40.078,
    'Fe': 55.845,
    'Cu': 63.546,
    'Zn': 65.38,
}

# 3. 몰질량 계산 함수
def calculate_molar_mass(parsed_formula):
    total = 0
    for elem, count in parsed_formula.items():
        if elem not in atomic_weights:
            raise ValueError(f"원자 '{elem}' 의 원자량 정보가 없습니다.")
        total += atomic_weights[elem] * count
    return total

# 4. Streamlit 앱
st.title("몰 계산기")

formula = st.text_input("화학식을 입력하세요 (예: C6H12O6, Fe2(SO4)3)")

mass = st.number_input("질량을 입력하세요 (g)", min_value=0.0)

if st.button("몰 수 계산"):
    try:
        parsed = parse_formula(formula)
        molar_mass = calculate_molar_mass(parsed)
        if molar_mass == 0:
            st.error("올바른 화학식을 입력하세요.")
        else:
            mol = mass / molar_mass
            st.success(f"몰질량: {molar_mass:.3f} g/mol")
            st.success(f"몰 수: {mol:.4f} mol")
    except ValueError as e:
        st.error(str(e))


