import re
import streamlit as st

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

atomic_weights = {
    'H': 1,
    'He': 4,
    'Li': 7,
    'Be': 9,
    'B': 11,
    'C': 12,
    'N': 14,
    'O': 16,
    'F': 18.998,
    'Ne': 20,
    'Na': 23,
    'Mg': 24,
    'Al': 27,
    'Si': 28,
    'P': 31,
    'S': 32,
    'Cl': 35,
    'Ar': 40,
    'K': 39,
    'Ca': 40,
    'Fe': 56,
    'Cu': 64,
    'Zn': 65,
}

def calculate_molar_mass(parsed_formula):
    total = 0
    for elem, count in parsed_formula.items():
        if elem not in atomic_weights:
            raise ValueError(f"원자 '{elem}' 의 원자량 정보가 없습니다.")
        total += atomic_weights[elem] * count
    return total

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


