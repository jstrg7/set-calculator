import streamlit as st
import validator_manager as vm
from consts import DEFAULT_UNIVERSAL_SET
import operations_parser as op


if "sets" not in st.session_state:
    st.session_state.sets = {"U": DEFAULT_UNIVERSAL_SET}
    st.session_state.expression = ''
    st.session_state.result = None
    st.session_state.u_is_users = False


def add_symbol(symbol):
    st.session_state.expression += symbol
    st.session_state.result = None


def add_backspace():
    if len(st.session_state.expression) <= 0: return
    st.session_state.expression = st.session_state.expression[:len(st.session_state.expression) - 1]
    st.session_state.result = None


def format_set_latex(elements: tuple) -> str:
    if elements is None:
        return ""
    if len(elements) == 0:
        return r"\varnothing"
    return r"\left\{" + ", ".join(map(str, elements)) + r"\right\}"


def create_operation():
    st.session_state.result = None
    if len(st.session_state.expression) == 0:
        st.error("Expression is null.")
        return
    if not vm.operations_is_valid(st.session_state.expression):
        st.error("Expression is not valid. Check brackets and operators.")
        return
    if not st.session_state.sets:
        st.error("You have not got any sets.")
        return

    expression = st.session_state.expression.replace(" ", "")
    set_map = dict(st.session_state.sets)
    try:
        result_in_letter = op.get_operation(expression, set_map)
        st.session_state.result = set_map.get(result_in_letter, ())
    except Exception as e:
        st.session_state.result = None
        st.error(f"Error: {e}")


st.header("Your sets")
with st.form("set_form", clear_on_submit=True):
    col1, col2 = st.columns([1, 5])
    name = col1.text_input("Set name", max_chars=1).strip()
    naming_warning = col1.caption("You can write only A-Z letters. If you write U, universal set will be changed.")
    elements = col2.text_input("Set elements", placeholder="for ex: 1,2,3")
    elements_warning = col2.caption("You can write only A-Z, a-z and numbers for 1000.")
    ok = st.form_submit_button("Add")
    if ok:
        is_successfull, error_message, input_set = vm.validate_set_input(name, elements)
        if not is_successfull:
            st.error(f"There is some problems with your input: {error_message}")
        else:
            st.session_state.sets[name] = input_set
            if name == 'U': st.session_state.u_is_users = True


if st.session_state.sets:
    st.subheader("Your sets:")
    for name, elements in st.session_state.sets.items():
        if name == 'U' and st.session_state.u_is_users == False: continue
        st.latex(rf"{name} = {format_set_latex(elements)}")
    if st.button("Clear all sets"):
        st.session_state.sets = {'U': DEFAULT_UNIVERSAL_SET}
        st.session_state.result = None
        st.session_state.u_is_users = False
        st.rerun()


st.header("Your expression")
con = st.container()
if st.session_state.expression:
    con.latex(vm.validate_expression_output(st.session_state.expression, to_latex=True))
if st.session_state.sets:
    cols = con.columns(len(st.session_state.sets), gap="small")
    i = 0
    for name in st.session_state.sets:
        cols[i].button(name, f"{name}_button", on_click=add_symbol, args=(name,), use_container_width=True)
        i += 1
cols_operands = con.columns(5, gap="small")
intersection_btn = cols_operands[0].button("∩", "intersection_button", on_click=add_symbol, args=('-',), use_container_width=True)
union_btn = cols_operands[1].button("∪", "union_button", on_click=add_symbol, args=('+',), use_container_width=True)
complement_btn = cols_operands[2].button("c", "complement_button", on_click=add_symbol, args=("'",), use_container_width=True)
diff_btn = cols_operands[3].button("/", "diff_button", on_click=add_symbol, args=('/',), use_container_width=True)
sym_dif_btn = cols_operands[4].button("△", "sym_diff_button", on_click=add_symbol, args=('%',), use_container_width=True)
cols_other_btns = con.columns(3, gap="small")
opened_br_btn = cols_other_btns[0].button("(", "opened_bracket_button", on_click=add_symbol, args=("(",), use_container_width=True)
closed_br_btn = cols_other_btns[1].button(")", "closed_bracket_button", on_click=add_symbol, args=(")",), use_container_width=True)
backspace_btn = cols_other_btns[2].button("Backspace", "backspace_button", on_click=add_backspace, use_container_width=True)
operations_cols = con.columns(2)
create_operation_btn = operations_cols[0].button("Create operation", "create_operation_button", on_click=create_operation, use_container_width=True)
if operations_cols[1].button("Clear all operations", use_container_width=True):
    st.session_state.expression = ''
    st.session_state.result = None


st.header("Your result")
if st.session_state.result is not None:
    st.latex(rf"\text{{Result}} = {format_set_latex(st.session_state.result)}")
else:
    st.latex("")