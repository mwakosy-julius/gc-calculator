import streamlit as st
import plotly.graph_objects as go

def calculate_gc_content(sequence, window_size=100):
    gc_content = []
    positions = []
    for i in range(0, len(sequence) - window_size + 1, window_size):
        window = sequence[i:i + window_size]
        gc_count = window.count('G') + window.count('C')
        gc_content.append((gc_count / window_size) * 100)
        positions.append(i)
    return positions, gc_content

def plot_gc_content(positions, gc_content, window_size):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=positions, y=gc_content,
        mode='lines+markers',
        name='GC Content',
        marker=dict(color='blue', size=6),
        line=dict(color='blue', width=2)
    ))
    fig.update_layout(
        title=f'GC Content Across Gene (Window size: {window_size} bp)',
        xaxis_title='Position in Gene',
        yaxis_title='GC Content (%)',
        template='plotly_white'
    )
    st.plotly_chart(fig)

def calculate_nucleotide_counts(sequence):
    total_length = len(sequence)
    counts = {
        'A': sequence.count('A'),
        'T': sequence.count('T'),
        'G': sequence.count('G'),
        'C': sequence.count('C')
    }
    percentages = {nuc: (count / total_length) * 100 for nuc, count in counts.items()}
    return total_length, counts, percentages

st.title("GC Content Calculator")

uploaded_file = st.file_uploader("Upload a Gene Sequence File (in FASTA or plain text format)", type=["txt", "fasta"])
window_size = st.number_input("Window size (bp)", min_value=10, value=100, step=10)

if uploaded_file:
    sequence = uploaded_file.read().decode("utf-8").replace("\n", "")
    # st.write(f"**Gene Sequence Length:** {len(sequence)} bp")

    positions, gc_content = calculate_gc_content(sequence, window_size)

    # st.subheader("GC Content Plot")
    plot_gc_content(positions, gc_content, window_size)

    total_length, counts, percentages = calculate_nucleotide_counts(sequence)
    summary = (
        f"Summary: Full Length({total_length} bp) | "
        f"A({percentages['A']:.1f}% {counts['A']}) | "
        f"T({percentages['T']:.1f}% {counts['T']}) | "
        f"G({percentages['G']:.1f}% {counts['G']}) | "
        f"C({percentages['C']:.1f}% {counts['C']})"
    )
    st.write(summary)

# gene_sequence = "ATGCGCATGCGATCGT" * 100  
# window_size = 100
# gc_content = calculate_gc_content(gene_sequence)
# plot_gc_content(gc_content, window_size)